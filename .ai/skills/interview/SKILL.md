---
name: interview
argument-hint: [instructions]
description: Interview user in-depth to create a detailed spec
allowed-tools: AskUserQuestion, Write
---

Follow the user instructions and interview me in detail using your harness's structured-question tool (AskUserQuestion on Claude Code, AskQuestion on Cursor, request_user_input on Codex) about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious. be very in-depth and continue interviewing me continually until it's complete. then, write the spec to a file. <instructions>$ARGUMENTS</instructions>
