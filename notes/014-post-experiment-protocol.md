# Post-Experiment Protocol

After completing any spawn experiment, follow this checklist to maintain project organization and extract research value.

## Immediate Actions (Within experiment folder)

### 1. Verify Experiment Completion
- [ ] All 4 methods completed successfully
- [ ] EXPERIMENT_REPORT.md generated with timing analysis
- [ ] Results validated and documented

### 2. Extract Research Findings
- [ ] Identify key insights from experiment results
- [ ] Determine if findings warrant new research finding document
- [ ] Create finding document in `notes/findings/` if significant

## Project-Level Updates

### 3. Update EXPERIMENT_INDEX.md
- [ ] Add new experiment entry with:
  - Full hierarchical number (T.DCC.V format)
  - Brief description
  - Version information (if re-run)
  - Completion status
  - Key results summary
  - Link to experiment report

### 4. Update README.md Homepage
- [ ] Add new experiment to "LATEST EXPERIMENT" section
- [ ] Move previous latest to appropriate historical section
- [ ] Update any relevant statistics or counters
- [ ] Include compelling headline/summary

### 5. Update FUTURE_EXPERIMENTS_ROADMAP.md
- [ ] Mark experiment as completed
- [ ] Add insights to roadmap notes
- [ ] Identify follow-up experiments if applicable
- [ ] Update priority rankings based on results

## Strategic Analysis (Private)

### 6. Business Framework Assessment
- [ ] Evaluate methodology performance for personal project applications
- [ ] Update methodology selection guidelines in personal framework
- [ ] Identify components for utils library curation
- [ ] Document productivity insights

### 7. Research Quality Assurance
- [ ] Verify timing measurement methodology was followed
- [ ] Confirm bias prevention protocols were observed
- [ ] Validate methodology authenticity in results
- [ ] Check for experimental design improvements

## Publication Workflow

### 8. Public Repository Sync
- [ ] Commit all changes to private repository
- [ ] Review what will be public vs private via gitignore
- [ ] Push to public repository for research sharing
- [ ] Verify public presentation is clean and professional

### 9. Follow-up Planning
- [ ] Schedule next experiment if pipeline is established
- [ ] Update research priorities based on findings
- [ ] Consider replication studies if results are significant
- [ ] Plan meta-analysis if enough data accumulated

## Quality Gates

**Do not mark experiment complete until:**
- All 4 methods have working implementations
- Timing data is accurate and validated
- Experiment report includes comparative analysis
- Project documentation is updated
- Research findings are captured

**Before public push:**
- Verify no private information in public-facing files
- Confirm professional presentation quality
- Validate all links and references work correctly

---

## Versioning Decisions

### When to Create New Version (T.DCC.1+)
- **Methodology Evolution**: Framework/prompt improvements warrant re-testing
- **Validation Studies**: Independent confirmation of controversial results
- **Environmental Changes**: Significant AI model updates affect outcomes
- **Bias Detection**: Multiple runs needed to establish consistency
- **Replication Research**: External validation requests

### Version Documentation Requirements
Each new version must include:
- **VERSION_NOTES.md** explaining purpose and changes
- **Comparison analysis** with base version results
- **Environmental documentation** (AI model, date, conditions)
- **Methodology changes** from previous version

### Base Version Preservation
- Never modify T.DCC.0 experiments after completion
- Archive represents historical methodology state
- Enables longitudinal research on methodology evolution

---

**Template Usage**: Copy this checklist for each experiment and check off items as completed to ensure consistent post-experiment workflow.