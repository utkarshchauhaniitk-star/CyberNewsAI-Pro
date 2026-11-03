import React from 'react';
import { 
  Radio, 
  LayoutDashboard, 
  Pin, 
  BarChart3, 
  Rss, 
  Cpu, 
  Zap,
  Globe2,
  Terminal,
  Activity
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, pinnedCount = 0 }) {
  const navItems = [
    { 
      id: 'feed', 
      label: 'Live Threat Stream', 
      icon: Radio, 
      tag: 'REAL-TIME',
      tagColor: 'var(--neon-green)'
    },
    { 
      id: 'dashboard', 
      label: 'SOC War Room', 
      icon: LayoutDashboard,
      tag: 'OVERVIEW'
    },
    { 
      id: 'pinned', 
      label: 'Pinned Threats', 
      icon: Pin, 
      badge: pinnedCount > 0 ? pinnedCount : null 
    },
    { 
      id: 'stats', 
      label: 'Threat Intelligence', 
      icon: BarChart3,
      tag: 'ANALYTICS' 
    },
    { 
      id: 'sources', 
      label: 'Monitored Feeds', 
      icon: Rss,
      tag: '5 FEEDS'
    },
  ];

  return (
    <aside style={{
      width: '270px',
      position: 'fixed',
      top: 0,
      left: 0,
      bottom: 0,
      background: 'rgba(5, 9, 18, 0.96)',
      borderRight: '1px solid var(--border-neon)',
      display: 'flex',
      flexDirection: 'column',
      padding: '1.5rem 1.1rem',
      zIndex: 50,
      backdropFilter: 'blur(16px)',
      boxShadow: '4px 0 25px rgba(0, 0, 0, 0.6)'
    }}>
      {/* Brand Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', padding: '0.5rem 0.5rem 1.75rem' }}>
        <div style={{
          width: '42px',
          height: '42px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, rgba(0, 242, 254, 0.25), rgba(168, 85, 247, 0.35))',
          border: '1px solid var(--neon-cyan)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 18px rgba(0, 242, 254, 0.35)'
        }}>
          <Activity size={24} color="var(--neon-cyan)" />
        </div>
        <div>
          <div style={{
            fontSize: '1.2rem',
            fontWeight: 800,
            letterSpacing: '0.04em',
            fontFamily: 'var(--font-sans)',
            background: 'linear-gradient(135deg, #00f2fe 10%, #00ff9d 60%, #a855f7 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            CYBERNEWS // AI
          </div>
          <div style={{
            fontSize: '0.66rem',
            color: 'var(--neon-cyan)',
            fontFamily: 'var(--font-mono)',
            letterSpacing: '0.08em',
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem'
          }}>
            <span className="live-beacon"></span> LIVE THREAT RADAR
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem', flex: 1 }}>
        <div style={{
          fontSize: '0.66rem',
          textTransform: 'uppercase',
          letterSpacing: '0.12em',
          color: 'var(--text-muted)',
          padding: '0.4rem 0.65rem',
          fontFamily: 'var(--font-mono)'
        }}>
          // TACTICAL CONSOLE
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.75rem 0.95rem',
                borderRadius: 'var(--radius-sm)',
                background: isActive 
                  ? 'linear-gradient(90deg, rgba(0, 242, 254, 0.18) 0%, rgba(12, 20, 36, 0.8) 100%)' 
                  : 'transparent',
                border: isActive ? '1px solid var(--neon-cyan)' : '1px solid transparent',
                color: isActive ? 'var(--neon-cyan)' : 'var(--text-secondary)',
                fontWeight: isActive ? 700 : 500,
                fontSize: '0.86rem',
                fontFamily: 'var(--font-mono)',
                cursor: 'pointer',
                transition: 'all 0.18s ease',
                boxShadow: isActive ? '0 0 15px rgba(0, 242, 254, 0.2)' : 'none',
                textAlign: 'left'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = '#fff';
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
                  e.currentTarget.style.border = '1px solid var(--border-dim)';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = 'var(--text-secondary)';
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.border = '1px solid transparent';
                }
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Icon size={18} color={isActive ? 'var(--neon-cyan)' : 'currentColor'} />
                <span>{item.label}</span>
              </div>
              
              {item.badge ? (
                <span style={{
                  background: 'var(--neon-purple)',
                  color: '#fff',
                  fontSize: '0.68rem',
                  fontWeight: 700,
                  padding: '0.15rem 0.5rem',
                  borderRadius: '12px',
                  boxShadow: '0 0 10px rgba(168, 85, 247, 0.6)'
                }}>
                  {item.badge}
                </span>
              ) : item.tag ? (
                <span style={{
                  fontSize: '0.62rem',
                  color: item.tagColor || 'var(--text-muted)',
                  border: `1px solid ${item.tagColor ? item.tagColor : 'rgba(255, 255, 255, 0.1)'}`,
                  padding: '0.1rem 0.35rem',
                  borderRadius: '3px'
                }}>
                  {item.tag}
                </span>
              ) : null}
            </button>
          );
        })}
      </nav>

      {/* Futuristic Telemetry Diagnostics Box */}
      <div style={{
        padding: '0.9rem',
        borderRadius: 'var(--radius-sm)',
        background: 'rgba(3, 6, 12, 0.85)',
        border: '1px solid var(--border-neon)',
        fontSize: '0.7rem',
        fontFamily: 'var(--font-mono)',
        boxShadow: 'inset 0 0 15px rgba(0, 242, 254, 0.05)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.45rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>STREAM BUFFER</span>
          <span style={{ color: 'var(--neon-green)', fontWeight: 700 }}>SYNCHRONIZED</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.45rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>INGESTION ENGINE</span>
          <span style={{ color: 'var(--neon-cyan)' }}>THREADPOOL-x5</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ color: 'var(--text-muted)' }}>PERSISTENCE</span>
          <span style={{ color: '#e2e8f0' }}>SQLITE WAL</span>
        </div>
      </div>
    </aside>
  );
}
