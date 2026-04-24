"""App templates — pre-built starting points for common app types."""

from pathlib import Path


# Faceless Content Creator Template
FACELESS_TEMPLATE = """
import Image from "next/image";
import { useState } from "react";

const niches = [
  { name: "Finance", cpm: "$15-25", emoji: "💰", color: "from-emerald-500 to-green-600" },
  { name: "Health", cpm: "$10-20", emoji: "🏋️", color: "from-rose-500 to-pink-600" },
  { name: "Tech", cpm: "$8-15", emoji: "💻", color: "from-blue-500 to-indigo-600" },
  { name: "Motivation", cpm: "$5-12", emoji: "🔥", color: "from-amber-500 to-orange-600" },
  { name: "Education", cpm: "$7-15", emoji: "📚", color: "from-violet-500 to-purple-600" },
  { name: "Travel", cpm: "$6-14", emoji: "✈️", color: "from-cyan-500 to-teal-600" },
];

const sampleTopics = {
  Finance: ["Passive income 2026", "Compound interest hack", "Crypto staking truth", "Index fund strategy", "Side hustle breakdown"],
  Health: ["Morning routine", "Mental health tips", "Sleep optimization", "Nutrition myths", "Workout hacks"],
  Tech: ["AI tools review", "Coding shortcuts", "Productivity apps", "Tech predictions", "Automation tips"],
  Motivation: ["Stoic wisdom", "Success habits", "Mindset shifts", "Daily discipline", "Goal setting"],
  Education: ["Science facts", "History secrets", "Psychology tricks", "Learning hacks", "Study methods"],
  Travel: ["Hidden gems", "Budget travel", "Digital nomad", "Luxury hacks", "Culture deep dives"],
};

export default function FacelessStudio() {
  const [selectedNiche, setSelectedNiche] = useState("Finance");
  const [topic, setTopic] = useState("");
  const [videos, setVideos] = useState([]);
  const [generating, setGenerating] = useState(false);

  const handleGenerate = () => {
    if (!topic.trim()) return;
    setGenerating(true);
    setTimeout(() => {
      const newVideo = {
        id: Date.now(),
        topic: topic,
        niche: selectedNiche,
        status: "ready",
        platforms: ["YouTube", "TikTok", "Instagram", "Facebook"],
      };
      setVideos([newVideo, ...videos]);
      setTopic("");
      setGenerating(false);
    }, 2000);
  };

  const handleBulkGenerate = () => {
    setGenerating(true);
    const topics = sampleTopics[selectedNiche] || [];
    const newVideos = topics.map((t, i) => ({
      id: Date.now() + i,
      topic: t,
      niche: selectedNiche,
      status: "ready",
      platforms: ["YouTube", "TikTok", "Instagram", "Facebook"],
    }));
    setTimeout(() => {
      setVideos([...newVideos, ...videos]);
      setGenerating(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-[#0a0a1a] text-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-white/10">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🎬</span>
          <span className="font-bold text-lg">Faceless Studio</span>
        </div>
        <div className="flex gap-4 text-sm text-gray-400">
          <span>Pipeline</span>
          <span className="text-white font-medium">Dashboard</span>
          <span>Niches</span>
          <span>Schedule</span>
        </div>
      </nav>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 min-h-[calc(100vh-64px)] border-r border-white/10 p-4">
          <h3 className="text-xs uppercase text-gray-500 mb-3">Top Niches</h3>
          <div className="space-y-2">
            {niches.map((niche) => (
              <button
                key={niche.name}
                onClick={() => setSelectedNiche(niche.name)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition ${
                  selectedNiche === niche.name
                    ? "bg-white/10 text-white"
                    : "text-gray-400 hover:bg-white/5"
                }`}
              >
                <span className="mr-2">{niche.emoji}</span>
                {niche.name}
                <span className="float-right text-xs text-green-400">{niche.cpm}</span>
              </button>
            ))}
          </div>

          <div className="mt-6 p-3 rounded-lg bg-white/5 border border-white/10">
            <p className="text-xs text-gray-400">Bulk Workflow</p>
            <p className="text-sm font-medium mt-1">2 hrs = 60 videos</p>
            <button
              onClick={handleBulkGenerate}
              disabled={generating}
              className="mt-2 w-full py-1.5 bg-green-600 hover:bg-green-700 rounded text-xs font-medium disabled:opacity-50"
            >
              {generating ? "Generating..." : "Bulk Generate"}
            </button>
          </div>
        </aside>

        {/* Main */}
        <main className="flex-1 p-6">
          {/* Pipeline */}
          <div className="flex items-center gap-3 mb-6 p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/20 text-blue-300 text-xs font-medium">
              💡 Idea
            </div>
            <span className="text-gray-600">→</span>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/20 text-purple-300 text-xs font-medium">
              📝 Script
            </div>
            <span className="text-gray-600">→</span>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-pink-500/20 text-pink-300 text-xs font-medium">
              🎤 Voice
            </div>
            <span className="text-gray-600">→</span>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/20 text-amber-300 text-xs font-medium">
              🎬 Video
            </div>
            <span className="text-gray-600">→</span>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/20 text-green-300 text-xs font-medium">
              📤 Post
            </div>
          </div>

          {/* Generate */}
          <div className="flex gap-3 mb-6">
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
              placeholder={`Enter ${selectedNiche.toLowerCase()} topic...`}
              className="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-gray-500 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleGenerate}
              disabled={generating || !topic.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium disabled:opacity-50"
            >
              {generating ? "⏳" : "Generate"}
            </button>
          </div>

          {/* Video Grid */}
          <h2 className="text-lg font-bold mb-4">
            Generated Videos
            <span className="ml-2 text-sm text-gray-500">({videos.length})</span>
          </h2>

          {videos.length === 0 ? (
            <div className="text-center py-20 text-gray-500">
              <p className="text-4xl mb-3">🎬</p>
              <p>No videos yet. Enter a topic to get started.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {videos.map((video) => (
                <div
                  key={video.id}
                  className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 transition"
                >
                  <div className="aspect-[9/16] bg-gradient-to-b from-gray-800 to-gray-900 rounded-lg mb-3 flex items-center justify-center">
                    <span className="text-3xl">🎥</span>
                  </div>
                  <h3 className="font-medium text-sm mb-1">{video.topic}</h3>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-green-400">✅ {video.status}</span>
                    <div className="flex gap-1">
                      {video.platforms.map((p) => (
                        <span key={p} className="text-xs px-1.5 py-0.5 rounded bg-white/10 text-gray-400">
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
"""

# SaaS Dashboard Template
SAAS_DASHBOARD_TEMPLATE = """
"use client";
import { useState } from "react";

const metrics = [
  { label: "MRR", value: "$12,450", change: "+14%", up: true },
  { label: "Users", value: "2,847", change: "+8%", up: true },
  { label: "Churn", value: "3.2%", change: "-0.5%", up: false },
  { label: "ARPU", value: "$4.37", change: "+2%", up: true },
];

export default function SaaSDashboard() {
  const [period, setPeriod] = useState("30d");
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="flex items-center justify-between px-6 py-4 border-b border-white/10">
        <span className="font-bold text-lg">📊 SaaS Dashboard</span>
        <div className="flex gap-2">
          {["7d", "30d", "90d"].map((p) => (
            <button key={p} onClick={() => setPeriod(p)}
              className={`px-3 py-1 rounded text-sm ${period === p ? "bg-blue-600" : "bg-white/5 hover:bg-white/10"}`}
            >{p}</button>
          ))}
        </div>
      </nav>
      <div className="p-6">
        <div className="grid grid-cols-4 gap-4 mb-6">
          {metrics.map((m) => (
            <div key={m.label} className="p-4 rounded-xl bg-white/5 border border-white/10">
              <p className="text-sm text-gray-400">{m.label}</p>
              <p className="text-2xl font-bold mt-1">{m.value}</p>
              <p className={`text-sm mt-1 ${m.up ? "text-green-400" : "text-red-400"}`}>{m.change}</p>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div className="col-span-2 p-6 rounded-xl bg-white/5 border border-white/10">
            <h3 className="font-bold mb-4">Revenue Trend</h3>
            <div className="h-48 flex items-end gap-2">
              {[40,65,45,80,55,90,70,85,60,95,75,88].map((h,i) => (
                <div key={i} className="flex-1 bg-blue-600 rounded-t" style={{height:`${h}%`}} />
              ))}
            </div>
          </div>
          <div className="p-6 rounded-xl bg-white/5 border border-white/10">
            <h3 className="font-bold mb-4">Top Plans</h3>
            <div className="space-y-3">
              {[["Pro", "1,234", "$29/mo"], ["Team", "456", "$79/mo"], ["Enterprise", "89", "$199/mo"]].map(([plan, count, price]) => (
                <div key={plan} className="flex justify-between items-center py-2 border-b border-white/5">
                  <div><p className="font-medium">{plan}</p><p className="text-xs text-gray-500">{count} users</p></div>
                  <span className="text-green-400 font-medium">{price}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

# Portfolio Template
PORTFOLIO_TEMPLATE = """
export default function Portfolio() {
  const projects = [
    { title: "AI Dashboard", desc: "Real-time analytics with ML insights", tech: "Next.js, Python", emoji: "🤖" },
    { title: "Crypto Tracker", desc: "Portfolio management with whale alerts", tech: "React, Node", emoji: "💰" },
    { title: "Voice App", desc: "Text-to-speech with cloned voices", tech: "Python, FastAPI", emoji: "🎤" },
  ];
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="flex items-center justify-between px-6 py-4 border-b border-white/10">
        <span className="font-bold">JD</span>
        <div className="flex gap-6 text-sm text-gray-400">
          <span className="text-white">Work</span><span>About</span><span>Contact</span>
        </div>
      </nav>
      <div className="max-w-4xl mx-auto py-20 px-6">
        <p className="text-sm text-blue-400 mb-2">Full-Stack Developer</p>
        <h1 className="text-5xl font-bold mb-4">Building tools<br />that ship.</h1>
        <p className="text-gray-400 text-lg mb-12 max-w-xl">I build AI-powered products and open-source tools. Currently focused on agents, voice AI, and developer experience.</p>
        <div className="grid grid-cols-3 gap-4">
          {projects.map((p) => (
            <div key={p.title} className="p-5 rounded-xl bg-white/5 border border-white/10 hover:border-blue-500/50 transition">
              <span className="text-3xl">{p.emoji}</span>
              <h3 className="font-bold mt-3">{p.title}</h3>
              <p className="text-sm text-gray-400 mt-1">{p.desc}</p>
              <p className="text-xs text-gray-500 mt-3">{p.tech}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""

TEMPLATES = {
    "faceless": {
        "name": "Faceless Content Studio",
        "description": "AI-powered faceless video creator: idea → script → voice → video → post",
        "code": FACELESS_TEMPLATE,
    },
    "saas-dashboard": {
        "name": "SaaS Dashboard",
        "description": "MRR, users, churn metrics with revenue charts and plan breakdown",
        "code": SAAS_DASHBOARD_TEMPLATE,
    },
    "portfolio": {
        "name": "Developer Portfolio",
        "description": "Clean portfolio with projects, about, and contact sections",
        "code": PORTFOLIO_TEMPLATE,
    },
}


def list_templates():
    """Return available template names and descriptions."""
    return {k: {"name": v["name"], "description": v["description"]} for k, v in TEMPLATES.items()}


def get_template(name: str) -> str | None:
    """Get template code by name."""
    tpl = TEMPLATES.get(name)
    return tpl["code"] if tpl else None