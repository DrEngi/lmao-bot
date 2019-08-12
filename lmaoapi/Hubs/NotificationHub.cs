using lmaocore.Models.SignalR;
using Microsoft.AspNetCore.SignalR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace lmaoapi.Hubs
{
    public class NotificationHub : Hub
    {
        public Task Notify(NotificationMsg msg)
        {
            return Clients.All.SendAsync("RecieveMessage", msg);
        }
    }
}
