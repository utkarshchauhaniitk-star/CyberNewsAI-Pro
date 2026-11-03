import React, { useState } from 'react';
import { 
  X, 
  ExternalLink, 
  Sparkles, 
  Pin, 
  ShieldAlert, 
  Calendar, 
  Bug, 
  Layers, 
  Copy, 
  Check, 
  AlertCircle,
  Activity
} from 'lucide-react';
import { summarizeArticle } from '../services/api';

export default function ArticleDetailModal({
  article,
  onClose,
  onTogglePin,
  onArticleUpdated
}) {
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [summaryData, setSummaryData] = useState(
    article?.ai_summary ? { summary: article.ai_summary, is_ai_generated: true } : null
  );
  const [copiedLink, setCopiedLink] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  if (!article) return null;

  const handleGenerateSummary = async () => {
    setIsSummarizing(true);
    setErrorMsg(null);
    try {
      const res = await summarizeArticle(article.id, 150);
      setSummaryData(res);
      if (onArticleUpdated) {
        onArticleUpdated({ ...article, ai_summary: res.summary, is_ai_summarized: true });
      }
    } catch (err) {
      setErrorMsg(err.message || 'Failed to generate AI threat analysis.');
    } finally {
      setIsSummarizing(false);
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(article.link);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  const severityClass = 
    article.severity === 'Critical' ? 'badge-critical' :
    article.severity === 'High' ? 'badge-high' :
    article.severity === 'Low' ? 'badge-low' : 'badge-medium';

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-cyber" onClick={(e) => e.stopPropagation()}>
        
        {/* Futuristic Modal Header */}
        <div style={{
          padding: '1.35rem 1.75rem',
          borderBottom: '1px solid var(--border-neon)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          gap: '1rem',
          background: 'rgba(8, 14, 26, 0.95)'
        }}>
          <div>
            <div style={{ display: 'flex', gap: '0.45rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span className={`clickable-badge ${severityClass}`}>{article.severity}</span>
              <span className="clickable-badge badge-source">{article.source}</span>
              <span className="clickable-badge" style={{ background: 'rgba(0, 242, 254, 0.08)', color: 'var(--neon-cyan)', borderColor: 'var(--border-neon)' }}>
                {article.category}
              </span>
              {article.cves?.map(cve => (
                <span key={cve} className="clickable-badge badge-cve">{cve}</span>
              ))}
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1.4, fontFamily: 'var(--font-sans)' }}>
              {article.title}
            </h2>
          </div>

          <button
            onClick={onClose}
            className="btn-cyber btn-cyber-sm btn-cyber-ghost"
            style={{ borderRadius: '50%', width: '34px', height: '34px', padding: 0 }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Scrollable Telemetry Body */}
        <div style={{
          padding: '1.75rem',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.35rem'
        }}>
          
          {/* Cyber Telemetry Grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '0.85rem',
            padding: '1rem',
            background: 'rgba(3, 6, 12, 0.7)',
            border: '1px solid var(--border-neon)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.78rem',
            fontFamily: 'var(--font-mono)'
          }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block' }}>PUBLISHED TIMESTAMP:</span>
              <span style={{ color: 'var(--text-primary)' }}>
                {article.published || 'Live Stream'}
              </span>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block' }}>VULNERABILITY ID:</span>
              <span style={{ color: 'var(--neon-purple)', fontWeight: 700 }}>
                {article.cves?.length > 0 ? article.cves.join(', ') : 'GENERAL TELEMETRY'}
              </span>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block' }}>REPORTING SOURCE:</span>
              <span style={{ color: 'var(--neon-cyan)', fontWeight: 700 }}>{article.source}</span>
            </div>
          </div>

          {/* AI Executive Threat Briefing */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(0, 242, 254, 0.08), rgba(168, 85, 247, 0.08))',
            border: '1px solid var(--neon-cyan)',
            borderRadius: 'var(--radius-md)',
            padding: '1.35rem',
            boxShadow: '0 0 25px rgba(0, 242, 254, 0.15)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Sparkles size={18} color="var(--neon-cyan)" />
                <span style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--neon-cyan)', fontFamily: 'var(--font-mono)' }}>
                  // AI THREAT INTELLIGENCE BRIEFING
                </span>
                <span className="clickable-badge" style={{ background: 'var(--neon-cyan-glow)', color: 'var(--neon-cyan)', fontSize: '0.65rem' }}>
                  GEMINI 3.5 FLASH
                </span>
              </div>

              {!summaryData && !isSummarizing && (
                <button
                  onClick={handleGenerateSummary}
                  className="btn-cyber btn-cyber-sm btn-cyber-primary"
                >
                  <Sparkles size={13} /> GENERATE BRIEFING
                </button>
              )}
            </div>

            {isSummarizing ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', padding: '1rem 0' }}>
                <span className="live-beacon"></span>
                <span style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
                  Processing incident telemetry with Google Gemini AI...
                </span>
              </div>
            ) : summaryData ? (
              <div>
                <p style={{ fontSize: '0.9rem', color: '#f1f5f9', lineHeight: 1.65, whiteSpace: 'pre-line' }}>
                  {summaryData.summary}
                </p>
                <div style={{
                  marginTop: '0.9rem',
                  paddingTop: '0.75rem',
                  borderTop: '1px solid rgba(255, 255, 255, 0.08)',
                  fontSize: '0.74rem',
                  color: 'var(--text-muted)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  fontFamily: 'var(--font-mono)'
                }}>
                  <AlertCircle size={14} color="var(--neon-cyan)" />
                  <span>{summaryData.source_disclaimer || "AI-generated summary based strictly on reported vendor facts."}</span>
                </div>
              </div>
            ) : (
              <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
                Click "Generate Briefing" to synthesize a concise, technical executive summary identifying threat actors, vectors, and defenses.
              </p>
            )}

            {errorMsg && (
              <div style={{ color: 'var(--neon-crimson)', fontSize: '0.8rem', marginTop: '0.6rem', fontFamily: 'var(--font-mono)' }}>
                {errorMsg}
              </div>
            )}
          </div>

          {/* Full Advisory Text Extract */}
          <div>
            <h4 style={{ fontSize: '0.88rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.65rem', fontFamily: 'var(--font-mono)' }}>
              // TECHNICAL ADVISORY TEXT EXTRACT
            </h4>
            <div style={{
              background: 'rgba(3, 6, 12, 0.85)',
              border: '1px solid var(--border-neon)',
              borderRadius: 'var(--radius-sm)',
              padding: '1.15rem',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.65,
              maxHeight: '260px',
              overflowY: 'auto',
              whiteSpace: 'pre-line'
            }}>
              {article.content || article.summary || "No additional text content available."}
            </div>
          </div>

        </div>

        {/* Modal Action Buttons (All Clickable!) */}
        <div style={{
          padding: '1.1rem 1.75rem',
          borderTop: '1px solid var(--border-neon)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '1rem',
          background: 'rgba(5, 9, 18, 0.98)'
        }}>
          {/* Clickable Pin Button */}
          <button
            onClick={() => onTogglePin(article.id)}
            className={`btn-cyber btn-cyber-sm ${article.is_pinned ? 'btn-cyber-primary' : 'btn-cyber-ghost'}`}
          >
            <Pin size={15} />
            {article.is_pinned ? 'PINNED IN VAULT' : 'PIN TO VAULT'}
          </button>

          <div style={{ display: 'flex', gap: '0.65rem' }}>
            {/* Clickable Copy URL */}
            <button
              onClick={handleCopyLink}
              className="btn-cyber btn-cyber-sm btn-cyber-ghost"
            >
              {copiedLink ? <Check size={14} color="var(--neon-green)" /> : <Copy size={14} />}
              {copiedLink ? 'COPIED' : 'COPY URL'}
            </button>

            {/* Clickable Safe Isolated Link */}
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-cyber btn-cyber-sm btn-cyber-live"
              style={{ textDecoration: 'none' }}
            >
              READ FULL REPORT <ExternalLink size={14} />
            </a>
          </div>
        </div>

      </div>
    </div>
  );
}
