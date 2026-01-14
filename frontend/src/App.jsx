import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [topic, setTopic] = useState('');
  const [style, setStyle] = useState('documentary');
  const [duration, setDuration] = useState(30);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const generateVideo = async () => {
    setLoading(true);
    setStatus('starting');
    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, video_style: style, duration }),
      });
      const data = await res.json();
      setJobId(data.id);
      pollStatus(data.id);
    } catch (e) {
      console.error(e);
      alert('Failed to start generation');
      setLoading(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/status/${id}`);
        const data = await res.json();
        
        setStatus(data.status);
        setProgress(data.progress || 0);
        
        if (data.status === 'completed') {
          clearInterval(interval);
          setVideoUrl(`http://localhost:8000${data.video_url}`);
          setLoading(false);
        } else if (data.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
          alert(`Generation Failed: ${data.error}`);
        }
      } catch (e) {
        console.error(e);
      }
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <header className="mb-10 text-center">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent mb-4">
          AI Video Generator
        </h1>
        <p className="text-gray-400">Turn your ideas into viral shorts instantly.</p>
      </header>

      <main className="w-full max-w-lg bg-zinc-900/50 p-8 rounded-2xl border border-zinc-800 shadow-2xl backdrop-blur-sm">
        {!jobId || status === 'failed' ? (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Topic / Idea</label>
              <textarea 
                className="w-full bg-black/50 border border-zinc-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-primary focus:outline-none transition-all"
                rows="3"
                placeholder="Ex: A futuristic city aimed at solving climate change..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Style</label>
                <select 
                  className="w-full bg-black/50 border border-zinc-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-primary focus:outline-none"
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                >
                  <option value="documentary">Documentary</option>
                  <option value="cinematic">Cinematic</option>
                  <option value="emotional">Emotional</option>
                  <option value="upbeat">Upbeat / Hype</option>
                  <option value="horror">Horror</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Duration (Sec)</label>
                <select 
                  className="w-full bg-black/50 border border-zinc-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-primary focus:outline-none"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                >
                  <option value={15}>15 Seconds</option>
                  <option value={30}>30 Seconds</option>
                  <option value={45}>45 Seconds</option>
                  <option value={60}>60 Seconds</option>
                </select>
              </div>
            </div>

            <button 
              onClick={generateVideo}
              disabled={!topic || loading}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
                !topic || loading 
                  ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-lg shadow-primary/20'
              }`}
            >
              {loading ? 'Generating...' : 'Generate Video ✨'}
            </button>
          </div>
        ) : (
          <div className="text-center space-y-6 animate-fade-in">
            {status === 'completed' && videoUrl ? (
              <div className="space-y-4">
                <div className="relative rounded-xl overflow-hidden shadow-2xl border border-zinc-700 aspect-[9/16] max-h-[60vh] mx-auto bg-black">
                   <video 
                     src={videoUrl} 
                     controls 
                     autoPlay 
                     className="w-full h-full object-contain"
                   />
                </div>
                <button 
                  onClick={() => { setJobId(null); setStatus(null); setVideoUrl(null); }}
                  className="text-sm text-gray-400 hover:text-white underline"
                >
                  Create Another
                </button>
              </div>
            ) : (
              <div className="py-10">
                <div className="mb-4">
                    <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto"></div>
                </div>
                <h3 className="text-xl font-semibold animate-pulse">{status === 'processing' ? 'Crafting your video...' : 'Initializing...'}</h3>
                <p className="text-zinc-500 mt-2 text-sm">{status === 'processing' ? 'Generating scripts, images, and voiceovers.' : 'Please wait.'}</p>
                
                {/* Progress Bar */}
                <div className="w-full bg-zinc-800 rounded-full h-2.5 mt-6 overflow-hidden">
                  <div className="bg-gradient-to-r from-primary to-accent h-2.5 rounded-full transition-all duration-500" style={{ width: `${progress}%` }}></div>
                </div>
                <p className="text-xs text-right mt-1 text-zinc-500">{progress}%</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
