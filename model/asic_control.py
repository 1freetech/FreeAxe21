REQUIRED_TELEMETRY = {
"detected_asic_count","accepted_shares","rejected_shares","asic_result_activity",
"domain_A_vout","domain_A_iout","domain_B_vout","domain_B_iout",
"vrm_temperature","input_voltage","input_current","cooling_interlock","fan_or_pump_tach"
}

def may_hash(asic_count, uart_ok, telemetry_ok, power_ok, cooling_ok, reset_released):
    return all((asic_count == 8, uart_ok, telemetry_ok, power_ok, cooling_ok, reset_released))

def fault_action(reason):
    return {"hashing":False, "reset":"ASSERT", "fault_latched":True, "reason":reason}

def validate_control_config(cfg):
    assert cfg["asic"]["count"] == 8
    assert len(cfg["chain"]["domain_A"]) == 4
    assert len(cfg["chain"]["domain_B"]) == 4
    assert set(cfg["telemetry"]["required"]) >= REQUIRED_TELEMETRY
    assert cfg["clock"]["status"] == "UNRESOLVED_PHYSICAL"
    assert cfg["chain"]["partial_chain_policy"].startswith("fail closed")
    return True
