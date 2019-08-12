using System;
using System.Collections.Generic;
using System.Text;

namespace lmaocore.Models.SignalR
{
    /// <summary>
    /// Message that informs bot when settings updated
    /// </summary>
    public class NotificationMsg
    {
        /// <summary>
        /// Server ID of updated data
        /// </summary>
        public long ServerID { get; set; }
    }
}
