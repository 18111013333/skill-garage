- [ ] Job description has no sensitive/confidential info
- [ ] Save Job ID for tracking
- [ ] Role is appropriate for public job boards
- [ ] **Note:** Jobs appear under Fuku AI's accounts, not your LinkedIn page; cannot edit/delete directly

## 🎯 When to Use

Use this skill when you need to:

- Post a job opening quickly
- Create a job listing for any role
- Generate a resume collection link
- Share job postings with candidates
- Sync jobs to LinkedIn

## 🛠️ Tools

### post_job ⭐

Implemented by `scripts/post_job.js`.

Post job opening to 20+ job boards. Returns immediately with Job ID.

#### Parameters

| Parameter            | Required | Type   | Description                                                                                     | Default                                                        |
| -------------------- | -------- | ------ | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `title`              | ✅ Yes   | string | Job title (min 4 characters)                                                                    | -                                                              |
| `city_query`         | ✅ Yes   | string | City/location (supports fuzzy match)                                                            | -                                                              |
| `description`        | ✅ Yes   | string | Job description                                                                                 | -                                                              |
| `email`              | ✅ Yes   | string | Email to receive resumes                                                                        | -                                                              |
| `company`            | ❌ No    | string | Company name                                                                                    | `"Your Company"`                                               |
| `industry`           | ❌ No    | string | Industry/field                                                                                  | `"General"`                                                    |
| `linkedinCompanyUrl` | ❌ No    | string | LinkedIn company page URL. Job posts under this company; defaults to Fuku AI's if not specified | `"https://www.linkedin.com/company/business-consulting-inter"` |

#### Response

Returns Job ID. **LinkedIn sync takes 5-60 minutes in background.**

---

### check_linkedin_status

Implemented by `scripts/post_job.js`.

Check LinkedIn sync status once. Returns URL if ready, or "Pending".

#### Parameters

| Parameter | Required | Type   | Description         | Example      |
| --------- | -------- | ------ | ------------------- | ------------ |
| `jobId`   | ✅ Yes   | string | The job ID to check | `"abcd2345"` |

---

## 🤖 AI Assistant Workflow

### ⚠️ REQUIRED: Post Job + Spawn Monitor (Two Steps)

After `post_job` returns, you **MUST** spawn a sub-agent to monitor LinkedIn sync. Do NOT skip this.

**Step 1: Post Job**

```
result = await post_job({ title, city_query, description, email, ... })
```

**Step 2: Spawn Monitor (REQUIRED)**

Extract jobId from result, then spawn sub-agent when `sessions_spawn` is available:

```javascript
// Extract jobId from post_job result
const jobIdMatch = result.match(/Job ID:\s*`?([a-zA-Z0-9-]+)`?/);
const jobId = jobIdMatch?.[1];

// Preferred: spawn sub-agent to monitor
await sessions_spawn({
  task: `Monitor LinkedIn sync for job ID "${jobId}". Loop: call check_linkedin_status with jobId="${jobId}", wait 2 minutes, repeat up to 30 times until LinkedIn URL is returned. Notify user when URL is available.`,
  mode: "run",
  cleanup: "delete",
});

// Tell user
("✅ Job posted! Job ID: `xxx`. LinkedIn monitoring has already started. I'll notify you when sync completes (5-60 min).");
```

**Fallback if `sessions_spawn` is unavailable:**

Continue monitoring using this skill's own execution path instead of stopping or asking the user whether to continue.

- Preferred fallback check command: `node scripts/post_job.js --check-linkedin-status "<jobId>"`
- If the runtime truly cannot automate follow-up in background, explicitly say background monitoring is unavailable in this runtime, but do **not** pretend the workflow is complete.

**⚠️ If you skip Step 2:**

- User will NOT receive LinkedIn URL
- Incomplete workflow

### Mandatory sub-agent rule

After `post_job` succeeds, you must immediately start a monitoring sub-agent before sending the final user-facing success response.

Required order:

1. Call `post_job`
2. Extract `jobId`
3. Start monitoring sub-agent
4. Only then send the success reply to the user

Do **not** claim LinkedIn monitoring is in progress unless the sub-agent has actually been started successfully.

Allowed user-facing response pattern:

- Confirm the job was posted
- Confirm that LinkedIn monitoring has already been started
- Later, send the LinkedIn URL when available

Forbidden:

- Offering monitoring as an optional next step
- Saying "I'll monitor it" before starting the sub-agent
- Saying "processing in background" if no monitoring sub-agent is running
- "If you want, I can check LinkedIn sync status"
- "Next I can help monitor LinkedIn"
- Any phrasing that makes the required follow-up sound optional

If sub-agent startup fails or is unavailable, explicitly tell the user that automatic monitoring could not be started in this runtime.

Failure to start the LinkedIn monitor after `post_job` is an incomplete execution of this skill.

---

## 📦 Installation

### Install via ClawHub

```bash
clawhub install post-job
```

After install, ensure dependencies are present:

```bash
cd skills/post-job
npm install
```

### Manual Installation

```bash
# Clone or download the skill
cd your-openclaw-workspace/skills

# Install dependencies
cd post-job
npm install
```

## 🔐 Security Notes

- **Email Privacy**: Resume emails are visible in job postings - use a dedicated hiring email
- **Rate Limiting**: API may have rate limits for high-volume posting

## 🐛 Troubleshooting

### Issue: Job posts but no confirmation

**Cause**: Response timeout or network issue

**Solution**: Check backend logs, verify API credentials, retry with `--force`

### Issue: City not recognized

**Cause**: City not in location database

**Solution**:

1. Check `assets/locations.json` for supported cities
2. Try alternative spelling (e.g., "New York" vs "NYC")
3. Add new city to database and republish

### Issue: Duplicate job postings

**Cause**: Multiple API calls due to retry logic

**Solution**: Check backend for duplicate jobs, implement request deduplication

## ❓ FAQ

**Q: Do I need a LinkedIn account?**
No — posts through Fuku AI relay, no binding required.

**Q: Can I delete/edit a posted job?**
No direct control — contact Fuku AI support with Job ID.

**Q: Is this safe for confidential hiring?**
No — use traditional channels for sensitive roles.

**Q: What if Fuku AI goes offline?**
Posting may fail or sync delayed; skill returns error.

## 🤝 Contributing

Found a bug or want to add more cities?

1. Fork the skill
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This skill is provided as-is for use with OpenClaw.

## 🆘 Support

For issues or questions:

- Check this SKILL.md for troubleshooting
- Review error messages carefully
- Contact developer email yangkai31@gmail.com if you run into any issues

---

**Happy Hiring! 🎉**
