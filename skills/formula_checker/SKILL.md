<tool>
  <purpose>Industrial-grade physics formula validation with dimensional analysis and numerical constant verification</purpose>
  
  <parameters>
    <param name="formula" type="string" required="true">
      Single physics formula to validate. Must contain exactly one '=' and use '^' for exponents.
      Example: "E = m * c^2"
    </param>
    <param name="batch" type="array" required="false">
      JSON array of formulas for batch processing. Each formula must follow single formula rules.
      Example: ["F = m * a", "E = m * c^2"]
    </param>
    <param name="values" type="object" required="false">
      Numerical values for constants to validate against physical standards.
      Example: {"c": 299792458, "h": 6.62607015e-34}
    </param>
  </parameters>

  <error-rules>
    <rule type="syntax_error" severity="critical">
      Reject formulas missing '=' or containing invalid characters.
      Validation: Formula must match pattern '[a-zA-Z0-9_]+\\s*=\\s*[a-zA-Z0-9_\\s\\*\\/\\^]+'
    </rule>
    <rule type="dimensional_mismatch" severity="critical">
      Reject if dimensional analysis shows inconsistency (tolerance: exact match).
      Example: Left side dimension [M][L]/[T]^2 vs right side [M][L]^2/[T]^2
    </rule>
    <rule type="numerical_mismatch" severity="critical">
      Reject if constant values deviate beyond 1e-10 relative error from defined physical standards.
      Example: c must be 299792458 m/s ± 1e-10
    </rule>
    <rule type="symbol_collision" severity="warning">
      Auto-resolve symbol conflicts using context (E=energy in physics contexts).
      Resolution: Prefer physics constants over mathematical constants
    </rule>
  </error-rules>

  <physical-constants>
    <constant name="c" value="299792458" unit="m/s" tolerance="1e-10" />
    <constant name="G" value="6.67430e-11" unit="m^3/kg/s^2" tolerance="1e-6" />
    <constant name="h" value="6.62607015e-34" unit="J*s" tolerance="1e-10" />
    <constant name="k" value="1.380649e-23" unit="J/K" tolerance="1e-10" />
  </physical-constants>
</tool>