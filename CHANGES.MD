# Changes in rewrite (so far)
* `lmao prefix` is no longer a prompt, instead it is set explicitly through `lmao prefix [newprefix]` or `lmao setprefix [newprefix]`.
* NOTE: I replaced `lmao chance` with `lmao setass` to make the command a bit more clear. Toggle now actually toggles, and on, off, and lotto remain the same. `lmao react` has been changed to `lmao setreact` as well.
* help significantly reworked so it no longer lags and spams you when you want assistance, instead it'll display all the commands you need in the channel where you asked for them, showing only the ones you have permission for.
* `lmao mute` is easier to use, and now notifies you when a member is no longer muted.
* `lmao ping` no longer shows latency as it was wholly inaccurate.
* `lmao info` no longer displays member count, useless. also cleaned it up
* `lmao remind` now asks for a time to be specified in `dd:hh:mm`, or `mm:ss`, or similar.
* `lmao draw`, `lmao guess` removed for now.
* lmao admin/adminlist and related commands have been removed from the bot because they were underused and not required. Most bot access can be given by applying the `manage messages` permission to users.
* custom commands removed, filters basically do the same thing.

# Behind the scenes changes
* all help commands have been moved to the new helpmodule, as it is extensive.
* `lmao uptime` moved to the new DevModule.
* `clap` moved to the new TextModule.
* reminders moved to the new RemindModule.
* the following dev commands have been removed because they either need to be reworked or are now useless: getmarkdown, getemoji, addemoji, displayguildcount