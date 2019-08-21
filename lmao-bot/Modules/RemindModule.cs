using Discord;
using Discord.Addons.Interactive;
using Discord.Commands;
using lmao_bot.Models.UserSettings;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class RemindModule : InteractiveBase
    {
        private DatabaseService Database;

        public RemindModule(DatabaseService database)
        {
            Database = database;
        }

        [Command("Remind")]
        [Alias("Remindme")]
        [Summary("Set a reminder to... remind you")]
        public async Task<RuntimeResult> Remind([Remainder]string reminder = "")
        {
            List<string> humor = new List<string>()
            {
                "Take cookies out of oven.",
                "Construct additional pylons.",
                "Download more RAM.",
                "Claim my free prize for being the millionth visitor."
            };

            Random rdm = new Random();
            int r = rdm.Next(humor.Count);

            if (reminder.Equals(""))
            {
                string reminderQuery = $"{Context.User.Mention} What do you want to be reminded for? e.g. `{humor[r]}`\n\n(_Psst:_ Say `cancel` to cancel the reminder.)";
                await ReplyAsync(reminderQuery);
                var reminderResponse = await NextMessageAsync(timeout: new TimeSpan(0, 0, 30));
                if (reminderResponse != null)
                {
                    reminder = reminderResponse.Content;
                    if (reminder.ToLower().Equals("cancel")) return CustomResult.FromSuccess("Canceled.");
                }
                else
                {
                    return CustomResult.FromError(Context.User.Mention + " You didn't reply in time.");
                }
            }

            await ReplyAsync($"{Context.User.Mention} When do you want to be reminded? e.g. `1:30:15` or `30:15`.\n\n(_Psst:_ You can specify the number of days, hours, and/or minutes. Say `cancel` to cancel the reminder.)");
            var timeResponse = await NextMessageAsync(timeout: new TimeSpan(0, 0, 30));
            if (timeResponse != null)
            {
                string text = timeResponse.Content;
                if (text.ToLower().Equals("cancel")) return CustomResult.FromSuccess("Canceled.");

                TimeSpan timeSpan;
                try
                {
                    timeSpan = TimeSpan.Parse(text);
                    DateTime dueDate = DateTime.Now;
                    dueDate = dueDate.Add(timeSpan);

                    await Database.GetUserSettings().AddReminder(new Reminder()
                    {
                        Created = DateTime.Now,
                        DueDate = dueDate,
                        Message = reminder
                    }, (long)Context.User.Id);

                    return CustomResult.FromSuccess(dueDate.ToLongDateString() + " " + dueDate.ToLongTimeString());
                }
                catch (Exception ex)
                {
                    return CustomResult.FromError(ex.Message);
                }
            }
            else
            {
                return CustomResult.FromError(Context.User.Mention + " You didn't reply in time.");
            }
        }

        [Command("reminders")]
        [Summary("List all my reminders")]
        public async Task Reminder()
        {
            List<Reminder> reminders = await Database.GetUserSettings().ListReminders((long)Context.User.Id);
            EmbedBuilder e = new EmbedBuilder()
            {
                Title = $"Reminders for {Context.User.Username}",
                Footer = new EmbedFooterBuilder()
                {
                    Text = "Use `lmao remind` to add more reminders!"
                },
                Color = Color.Orange
            };

            foreach (Reminder r in reminders)
            {
                e.AddField(new EmbedFieldBuilder()
                {
                    Name = $"Reminder for {r.DueDate.ToUniversalTime().ToShortDateString()} {r.DueDate.ToUniversalTime().ToShortTimeString()} UTC",
                    Value = r.Message
                });
            }
            await ReplyAsync(embed: e.Build());
        }
    }
}
