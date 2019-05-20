using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Attributes
{
    [System.AttributeUsage(System.AttributeTargets.Method, AllowMultiple = false)]
    public class HiddenCommandAttribute : Attribute
    {
        public HiddenCommandAttribute()
        {

        }
    }
}
