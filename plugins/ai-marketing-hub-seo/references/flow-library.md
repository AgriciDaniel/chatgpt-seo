# FLOW route library

Framework and prompt routes adapted from Daniel Agrici, CC BY 4.0:
https://github.com/AgriciDaniel/flow. This adaptation uses the FLOW files
retained in the pinned public Claude SEO tree. The `flow_material` entry in
provenance records that parent commit, source directory and lock-file digest.
A separate current FLOW repository commit was not captured.

All 41 source routes are retained as a normalized catalog. In this retained snapshot, 38
route files share one generic stage worksheet; the three Win bodies are
distinct. This library maps those routes to concrete bundled SEO workflows
and preserves the useful Win outputs without duplicating generic prompts.

Read only the selected route and its referenced skill/template. Use known
business/asset facts, audience and locale, existing sources, constraints and
required sources. Missing measurements remain unknown. An ambiguous generic
route needs its stage and actual task, not an assumed full audit.

| Stage | Route | Deliverable / decision | Workflow | Template |
| --- | --- | --- | --- | --- |
| find | content-planning-for-topical-relevance-prompt | Content planning for Topical Relevance Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-cluster](../skills/seo-cluster/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| find | content-prioritization-prompt | Content Prioritization Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-plan](../skills/seo-plan/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| find | keyword-research-prompt | Keyword research prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-cluster](../skills/seo-cluster/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| find | keyword-variations-for-topical-relevance-prompt | Keyword variations for topical relevance prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-cluster](../skills/seo-cluster/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| find | prompt-audience-avatar | Prompt: Audience Avatar; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-sxo](../skills/seo-sxo/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| leverage | backlink-competition-prompt | Backlink competition prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-backlinks](../skills/seo-backlinks/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | ai-homepage-rewrite-prompt | AI Homepage Rewrite Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-local](../skills/seo-local/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | claude-deep-research-prompt | Content Research Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-local](../skills/seo-local/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | gbp-categories-prompt | GBP Categories Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-maps](../skills/seo-maps/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | gbp-description-claude-prompt-1 | GBP Description Content Prompt 1; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-maps](../skills/seo-maps/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | gbp-description-claude-prompt-2 | GBP Description Content Prompt 2; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-maps](../skills/seo-maps/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | gbp-description-claude-prompt-3 | GBP Description Content Prompt 3; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-maps](../skills/seo-maps/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | gbp-services-prompt | GBP Services Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-maps](../skills/seo-maps/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | prompt-generating-a-meta-description | Prompt: Generating a Meta Description; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-page](../skills/seo-page/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | prompt-generating-a-title-tag | Prompt: Generating a Title Tag; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-page](../skills/seo-page/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | prompt-rewriting-existing-homepage | Prompt: Rewriting Existing Homepage; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-local](../skills/seo-local/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| local | prompt-rewriting-existing-service-page | Prompt : Rewriting Existing Service Page; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-local](../skills/seo-local/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | ai-detector-test-follow-up-prompt | AI detector test follow-up Prompt; Review usefulness and evidence; detector results do not prove authorship. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | ai-supporting-pages-rewrite-prompt | AI Supporting Pages Rewrite Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-programmatic](../skills/seo-programmatic/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | basic-prompt | Basic Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | blog-post-outline-prompt | Blog Post Outline Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content-brief](../skills/seo-content-brief/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | blog-post-writing-prompt | Blog Post Writing Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | claude-prompt-1 | Content Prompt 1; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | claude-prompt-2 | Content Prompt 2; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | ctr-audit-prompt | CTR AUDIT PROMPT; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-google](../skills/seo-google/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | follow-up-prompt-1 | Follow-up Prompt 1; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | follow-up-prompt-2 | Follow-up Prompt 2; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | follow-up-prompt | Follow-up Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | paa-question-rewording-prompt | PAA Question Rewording Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | prompt-core-30-content-audit | Prompt: Core 30 Content Audit; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | property-content-with-authority-audit-prompt | Property content with authority audit prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | reddit-claude-prompt | Reddit Content Prompt; Use inspected public audience language; no posting or outreach. | [seo-content](../skills/seo-content/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | schema-prompt-1 | Schema Prompt 1; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-schema](../skills/seo-schema/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | step-1-the-chatgpt-discovery-prompt | Step 1: The ChatGPT Discovery Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-geo](../skills/seo-geo/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | step-2-the-follow-up-qualifying-prompt | Step 2: The Follow-Up Qualifying Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-geo](../skills/seo-geo/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | technical-audit-prompt | Technical Audit Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-technical](../skills/seo-technical/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | visibility-follow-up-prompt | Visibility Follow Up Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-geo](../skills/seo-geo/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| optimize | visiblity-prompt | Visiblity Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-geo](../skills/seo-geo/SKILL.md) | [Worksheet](../assets/flow-stage-worksheet.md) |
| win | bofu-page-brief-generator | BOFU Page Brief Generator; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-sxo](../skills/seo-sxo/SKILL.md) | [Worksheet](../assets/flow-win-bofu.md) |
| win | conversion-audit-prompt | Conversion Audit Prompt; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-sxo](../skills/seo-sxo/SKILL.md) | [Worksheet](../assets/flow-win-conversion.md) |
| win | dual-surface-content-scorecard | Dual-Surface Content Scorecard; Apply the stage worksheet with the selected domain workflow and real inputs. | [seo-sxo](../skills/seo-sxo/SKILL.md) | [Worksheet](../assets/flow-win-dual-surface.md) |

## Win templates

- [Buyer decision brief](../assets/flow-win-bofu.md): offer, audience, objections, proof, sections and appropriate next action.
- [Conversion path review](../assets/flow-win-conversion.md): actual friction, lead quality and measurement evidence.
- [Search and AI discovery review](../assets/flow-win-dual-surface.md): separately assessed readiness and measured outcomes.

The [machine-readable route catalog](../assets/flow-routes.json) records source
paths and dispatch mappings. No sync command, remote prompt fetch, claimed
performance gain or Claude runtime is required.
