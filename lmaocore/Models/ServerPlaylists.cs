using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmaocore.Models.ServerPlaylists
{
    class Server
    {
        public ObjectId _id { get; set; }
        public Int64 ServerID { get; set; }
        public Dictionary<string, Playlist> Playlists { get; set; }

    }

    class Playlist
    {
        public string PlaylistName { get; set; }
        public DateTime LastModified { get; set; }
        public List<Video> Videos { get; set; }
    }

    class Video
    {
        public string WebpageURL { get; set; }
        public string Requester { get; set; }
        public string Title { get; set; }
        public int Duration { get; set; }
        public string URL { get; set; }
        public string Uploader { get; set; }
        public string UploadDate { get; set; }
        public string ID { get; set; }
        public string Extractor { get; set; }
        public string Extension { get; set; }
    }
}
