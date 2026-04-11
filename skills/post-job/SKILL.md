---
name: post-job
description: Post free job ads to 20+ job boards such as LinkedIn, Indeed, Ziprecruiter etc. to receive applicant resumes via email.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "install-deps",
              "kind": "run",
              "label": "Install post-job dependencies",
              "command": "npm install"
            }
          ]
      }
  }
---

# JobPoster Skill

> ⚠️ **CRITICAL: Use this skill's canonical execution entrypoints for all job posting actions.**
>
> **Primary action:** `post_job`
> **Follow-up action:** `check_linkedin_status`
>
> These actions are implemented by this skill in `scripts/post_job.js`.
> Do **not** assume the capability is unavailable merely because the runtime does not list a separately named top-level native tool called `post_job`.
>
> **DO NOT** call internal APIs directly (`genJD`, `postToLinkd`, `API_URL_*`).
> **DO NOT** bypass `post_job` to call Fuku AI endpoints manually.
> **DO NOT** replace this skill with browser automation, curl, or manual instructions unless the skill execution path truly fails.
>
> **Why?** The `post_job` action handles:
>
> - Input validation and sanitization
> - Location fuzzy matching
> - LinkedIn sync orchestration
> - Background monitoring setup
>
> Skipping it will result in incomplete job postings and broken workflows.

## Runtime Requirements

This skill requires:

- `node` to run `scripts/post_job.js`
- `npm` to install dependencies from `package.json`
- Installed local dependencies (for example `axios`, `fuse.js`, `dayjs`)

If the skill is installed without dependencies, run `npm install` in the skill directory before using the script entrypoints.

## Execution Model

`post-job` is the skill/package name.
`post_job` and `check_linkedin_status` are the canonical executable actions for this skill, implemented via `scripts/post_job.js`.

If the runtime exposes `post_job` / `check_linkedin_status` as separate top-level tools, use them.
If the runtime does **not** expose separately named top-level tools, use this skill's script entrypoint directly instead of refusing:

- Post job: `node scripts/post_job.js --title "..." --city "..." --description "..." --company "..." --email "..." --linkedinCompanyUrl "..."`
- Check LinkedIn status: `node scripts/post_job.js --check-linkedin-status "<jobId>"`

Do **not** conclude the capability is unavailable solely because a same-named native tool is absent from the global tool list.

When the user asks to publish a job:

1. Use `post_job` as the primary execution path
2. If no separately exposed top-level `post_job` tool exists, invoke the script entrypoint in `scripts/post_job.js`
3. Use `check_linkedin_status` only for LinkedIn sync follow-up / monitoring
4. If no separately exposed top-level `check_linkedin_status` tool exists, use `node scripts/post_job.js --check-linkedin-status "<jobId>"`
5. Do **not** refuse solely because a same-named top-level tool is not visibly listed in the session tool list
6. Do **not** substitute manual posting instructions for actual execution unless this skill's execution path genuinely fails

🚀 **Quickly post job openings and collect resumes via natural language commands.**

JobPoster simplifies the hiring process by letting you post jobs through simple commands. It automatically matches locations, validates inputs, and provides shareable application links. Perfect for recruiters, hiring managers, and HR teams.

## ✨ Features

- **Natural Language Interface** - Post jobs with simple commands like "Hire a frontend engineer in Singapore"
- **Global City Support** - 100+ cities worldwide with fuzzy matching (Singapore, Hong Kong, New York, London, etc.)
- **AI Job Description** - Optional AI-powered JD generation for professional, compelling postings
- **Instant Application Links** - Get shareable URLs for candidates to apply directly
- **Resume Collection** - All applications sent to your specified email
- **LinkedIn Sync** - Automatic LinkedIn job posting integration

## ⚠️ External Service Notice

This skill uses **Fuku AI** (https://hapi.fuku.ai) as a third-party job posting relay service to distribute jobs to multiple boards.

Uses **Fuku AI** relay service — no LinkedIn account binding required. Jobs post anonymously through Fuku AI's infrastructure.

**Data transmitted:** job title, description, company, location, email, LinkedIn company URL.

## 🔒 Quick Checklist

- [ ] Use dedicated hiring email (not personal)

## 详细文档

请参阅 [references/details.md](references/details.md)
