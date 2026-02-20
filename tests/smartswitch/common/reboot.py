import json
import logging
import re
import time
import pytest
from multiprocessing.pool import ThreadPool
from tests.common.reboot import reboot_ss_ctrl_dict as reboot_dict, REBOOT_TYPE_HISTOYR_QUEUE, \
    sync_reboot_history_queue_with_dut, execute_reboot_smartswitch_command
from tests.common.utilities import wait_until
from tests.common.platform.device_utils import check_dpu_reachable_from_npu
from tests.gnmi.helper import gnoi_request_dpu

logger = logging.getLogger(__name__)

REBOOT_TYPE_COLD = "cold"
REBOOT_TYPE_UNKNOWN = "unknown"
REBOOT_TYPE_KERNEL_PANIC = "Kernel Panic"
REBOOT_TYPE_WATCHDOG = "Watchdog"

# gNOI DPU reboot constants
_GNOI_REBOOT_METHOD_COLD = 1
_GNOI_DPU_REBOOT_MESSAGE = "gNOI cold reboot test"
_GNOI_DPU_REBOOT_MAX_RETRIES = 3
_GNOI_DPU_REBOOT_RETRY_BACKOFF_SEC = 10
_GNOI_DPU_REBOOT_READINESS_TIMEOUT_SEC = 300
_GNOI_DPU_REBOOT_READINESS_INTERVAL_SEC = 15
_GNOI_REBOOT_CONNECTION_DROP_TERMS = (
    "unavailable", "connection reset", "eof",
    "transport closing", "broken pipe",
)


def log_and_perform_reboot(duthost, reboot_type, dpu_name):
    """
    Logs and initiates the reboot process based on the host type.
    Skips the test if the host is a DPU.

    @param duthost: DUT host object
    @param reboot_type: Type of reboot to perform
    @param dpu_name: Name of the DPU (optional)
    """
    hostname = duthost.hostname

    if reboot_type == REBOOT_TYPE_COLD:
        if duthost.dut_basic_facts()['ansible_facts']['dut_basic_facts'].get("is_smartswitch"):
            if dpu_name is None:
                logger.info("Sync reboot cause history queue with DUT reboot cause history queue")
                sync_reboot_history_queue_with_dut(duthost)

                with ThreadPool(processes=1) as pool:
                    async_result = pool.apply_async(execute_reboot_smartswitch_command,
                                                    (duthost, reboot_type, hostname))
                    pool.terminate()

                return {"failed": False,
                        "result": async_result}

            else:
                logger.info("Rebooting the DPU {} with type {}".format(dpu_name, reboot_type))
                return duthost.command("sudo reboot -d {}".format(dpu_name))
        elif duthost.facts['is_dpu']:
            pytest.skip("Skipping the reboot test as the DUT is a DPU")
    else:
        pytest.skip("Skipping the reboot test as the reboot type {} is not supported".format(reboot_type))


def log_and_perform_gnoi_reboot_dpu(duthost, dpu_index, dpu_name,
                                     method=_GNOI_REBOOT_METHOD_COLD,
                                     message=_GNOI_DPU_REBOOT_MESSAGE):
    """
    Sends a gNOI System.Reboot request to a DPU with retry/backoff.

    A connection drop / UNAVAILABLE response is treated as success — the DPU
    tears down the channel as soon as it begins rebooting.

    @param duthost:   DUT host object
    @param dpu_index: DPU index (0-based integer)
    @param dpu_name:  DPU name for logging (e.g. "DPU0")
    @param method:    gNOI RebootMethod enum value (default COLD=1)
    @param message:   Reboot reason string recorded on the device

    Returns:
        {"failed": False} if reboot was initiated
        {"failed": True, "message": <reason>} if all retries failed
    """
    logger.info("Initiating gNOI reboot for DPU %s (index=%d) method=%d",
                dpu_name, dpu_index, method)

    reboot_args = json.dumps({"method": method, "message": message})

    for attempt in range(1, _GNOI_DPU_REBOOT_MAX_RETRIES + 1):
        try:
            ret, msg = gnoi_request_dpu(
                duthost, None, dpu_index, "System", "Reboot", reboot_args
            )
        except Exception as e:
            ret, msg = -1, str(e)

        if ret == 0 or any(t in msg.lower() for t in _GNOI_REBOOT_CONNECTION_DROP_TERMS):
            logger.info("gNOI reboot initiated for %s (attempt %d/%d ret=%d)",
                        dpu_name, attempt, _GNOI_DPU_REBOOT_MAX_RETRIES, ret)
            return {"failed": False}

        logger.warning("gNOI reboot attempt %d/%d failed for %s rc=%d msg='%s'",
                       attempt, _GNOI_DPU_REBOOT_MAX_RETRIES, dpu_name, ret, msg.strip())

        if attempt < _GNOI_DPU_REBOOT_MAX_RETRIES:
            time.sleep(_GNOI_DPU_REBOOT_RETRY_BACKOFF_SEC * attempt)

    return {"failed": True,
            "message": "gNOI reboot RPC failed after {} attempts for {}".format(
                _GNOI_DPU_REBOOT_MAX_RETRIES, dpu_name)}

            
def perform_gnoi_reboot_dpu(duthost, dpu_index, dpu_name,
                             method=_GNOI_REBOOT_METHOD_COLD,
                             message=_GNOI_DPU_REBOOT_MESSAGE):
    """
    Performs a gNOI cold reboot on a DPU and waits for it to come back online.

    @param duthost:   DUT host object
    @param dpu_index: DPU index (0-based integer)
    @param dpu_name:  DPU name (e.g. "DPU0")
    @param method:    gNOI RebootMethod enum value (default COLD=1)
    @param message:   Reboot reason string

    Returns:
        True  — reboot initiated and DPU came back online
        False — reboot trigger failed or DPU did not come back within timeout
    """
    res = log_and_perform_gnoi_reboot_dpu(duthost, dpu_index, dpu_name, method, message)

    if res["failed"]:
        logger.error("gNOI reboot trigger failed for %s: %s", dpu_name, res["message"])
        return False

    logger.info("Waiting for %s (index=%d) to come back online (timeout=%ds)...",
                dpu_name, dpu_index, _GNOI_DPU_REBOOT_READINESS_TIMEOUT_SEC)

    came_up = wait_until(
        _GNOI_DPU_REBOOT_READINESS_TIMEOUT_SEC,
        _GNOI_DPU_REBOOT_READINESS_INTERVAL_SEC,
        0,
        check_dpu_reachable_from_npu,
        duthost, dpu_name, dpu_index,
    )

    if not came_up:
        logger.error("%s did not come back online within %ds after gNOI reboot",
                     dpu_name, _GNOI_DPU_REBOOT_READINESS_TIMEOUT_SEC)
        return False

    logger.info("gNOI reboot complete: %s is back online", dpu_name)
    return True


def perform_reboot(duthost, reboot_type=REBOOT_TYPE_COLD, dpu_name=None, invocation_type="cli_based", localhost=None):
    """
    Performs a reboot and validates the DPU status after reboot.

    @param duthost: DUT host object
    @param reboot_type: Reboot type
    @param dpu_name: DPU name
    @param invocation_type: Invocation type
    @param localhost: Localhost object
    """
    if reboot_type not in reboot_dict:
        pytest.skip("Skipping the reboot test as the reboot type {} is not supported".format(reboot_type))

    if invocation_type == "gnoi_based":
        if dpu_name is None:
            pytest.skip("gNOI-based reboot is not yet supported for switch-level reboot")
        if localhost is None:
            pytest.fail("localhost is required for gnoi_based invocation_type.")
        logger.info(
            "[gNOI] perform_reboot: dpu_name=%s reboot_type=%s",
            dpu_name, reboot_type,
        )
        dpu_index = int(re.search(r'\d+', dpu_name).group())
        success = perform_gnoi_reboot_dpu(duthost, dpu_index, dpu_name)
        if not success:
            pytest.fail("gNOI cold reboot failed for DPU {}".format(dpu_name))
    else:
        res = log_and_perform_reboot(duthost, reboot_type, dpu_name)
        if res and res['failed'] is True:
            if dpu_name is None:
                pytest.fail("Failed to reboot the {} with type {}".format(duthost.hostname, reboot_type))
            else:
                pytest.fail("Failed to reboot the DPU {} with type {}".format(dpu_name, reboot_type))

        if dpu_name is None:
            logger.info("Appending the last reboot type to the queue")
            REBOOT_TYPE_HISTOYR_QUEUE.append(reboot_type)
