using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Models.UserSettings
{
    public class LmaoBotUser
    {
        public ObjectId _id { get; set; }
        public Int64 UserID { get; set; }
        public Settings Settings { get; set; }
        public List<Reminder> Reminders { get; set; }
    }

    public class Settings
    {
        public int LmaoCount { get; set; }
    }

    public class Reminder
    {
        public DateTime Created { get; set; }
        public DateTime DueDate { get; set; }
        public string Message { get; set; }
    }
}
