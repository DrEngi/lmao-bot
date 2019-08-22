# Changes in rewrite (so far)
* `lmao prefix` is no longer a prompt, instead it is set explicitly through `lmao prefix [newprefix]` or `lmao setprefix [newprefix]`.
* NOTE: I replaced `lmao chance` with `lmao setass` to make the command a bit more clear. Toggle now actually toggles, and on, off, and lotto remain the same. `lmao react` has been changed to `lmao setreact` as well.
* help significantly reworked so it no longer lags and spams you when you want assistance, instead it'll display all the commands you need in the channel where you asked for them, showing only the ones you have permission for.
* `lmao ping` no longer shows latency as it was wholly inaccurate.
* `lmao info` no longer displays member count, useless. also cleaned it up
* `lmao remind` now asks for a time to be specified in `dd:hh:mm`, or `mm:ss`, or similar.
* `lmao draw`, `lmao guess` removed for now.

# Behind the scenes changes
* all help commands have been moved to the new helpmodule, as it is extensive.
* `lmao uptime` moved to the new DevModule.
* `clap` moved to the new TextModule.
* reminders moved to the new RemindModule.