using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Utilities
{
    public static class MessageUtil
    {
        public static string CleanMention(string message)
        {
            message = message.Replace("@here", "@\u200bhere");
            message = message.Replace("@everyone", "@\u200beveryone");
            return message;
        }
    }
}
