import React, { useState, useEffect, useCallback, useRef } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardView from './components/DashboardView';
import NewsFeedView from './components/NewsFeedView';
import ThreatStatsView from './components/ThreatStatsView';
import SourcesView from './components/SourcesView';
import ArticleDetailModal from './components/ArticleDetailModal';

import { 
  fetchArticles, 
  fetchThreatStats, 
  fetchCategories, 
  fetchSources, 
  refreshNewsFeeds,
  togglePinArticle 
} from './services/api';

export default function App() {
  // Default to the Live Threat Radar feed as requested
  const [activeTab, setActiveTab] = useState('feed');
  
  // Articles Feed State
  const [articles, setArticles] = useState([]);
  const [totalArticles, setTotalArticles] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedSource, setSelectedSource] = useState('All');
  const [selectedSeverity, setSelectedSeverity] = useState('All');
  const [hasCveFilter, setHasCveFilter] = useState(null);
  const [pinnedOnlyFilter, setPinnedOnlyFilter] = useState(null);
  const [categories, setCategories] = useState(['All']);
  const [sources, setSources] = useState(['All']);
  const [isLoadingArticles, setIsLoadingArticles] = useState(false);

  // Threat Stats State
  const [threatStats, setThreatStats] = useState(null);
  
  // Active Article Modal State
  const [activeArticleModal, setActiveArticleModal] = useState(null);

  // Global Refresh State & Auto Poll
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [autoPoll, setAutoPoll] = useState(false);
  const [lastSyncTime, setLastSyncTime] = useState(null);

  // Toast notifications
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  // Load Metadata & Stats on mount
  useEffect(() => {
    loadMetadata();
    loadThreatStats();
  }, []);

  const loadMetadata = async () => {
    try {
      const [cats, srcs] = await Promise.all([
        fetchCategories().catch(() => ['All']),
        fetchSources().catch(() => ['All'])
      ]);
      setCategories(cats);
      setSources(srcs);
    } catch (e) {
      console.error('Failed to load metadata', e);
    }
  };

  const loadThreatStats = async () => {
    try {
      const data = await fetchThreatStats();
      setThreatStats(data);
    } catch (e) {
      console.error('Failed to load threat stats', e);
    }
  };

  // Load Articles when query parameters change
  const loadArticles = useCallback(async () => {
    setIsLoadingArticles(true);
    try {
      const isPinnedTab = activeTab === 'pinned';
      const data = await fetchArticles({
        q: searchQuery,
        category: selectedCategory,
        source: selectedSource,
        severity: selectedSeverity,
        has_cve: hasCveFilter,
        pinned_only: isPinnedTab ? true : pinnedOnlyFilter,
        page,
        limit: 12
      });
      setArticles(data.items || []);
      setTotalArticles(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (e) {
      console.error('Failed to fetch articles', e);
      showToast('Could not reach backend API. Check server status.', 'error');
    } finally {
      setIsLoadingArticles(false);
    }
  }, [searchQuery, selectedCategory, selectedSource, selectedSeverity, hasCveFilter, pinnedOnlyFilter, activeTab, page]);

  useEffect(() => {
    loadArticles();
  }, [loadArticles]);

  // LIVE NEWS REFRESH FROM THE INTERNET
  const handleRefreshFeeds = async () => {
    setIsRefreshing(true);
    try {
      const res = await refreshNewsFeeds();
      setLastSyncTime(new Date().toLocaleTimeString());
      showToast(res.message || 'Live feeds synchronized in real time!', 'success');
      // Refresh current articles and stats immediately
      await Promise.all([loadArticles(), loadThreatStats()]);
    } catch (err) {
      showToast(err.message || 'Failed to refresh live feeds.', 'error');
    } finally {
      setIsRefreshing(false);
    }
  };

  // Auto-Poll Interval (60s)
  useEffect(() => {
    let intervalId = null;
    if (autoPoll) {
      intervalId = setInterval(() => {
        handleRefreshFeeds();
      }, 60000);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [autoPoll]);

  // Toggle Pinned Status on Article
  const handleTogglePin = async (id) => {
    try {
      const res = await togglePinArticle(id);
      setArticles(prev => prev.map(a => a.id === id ? { ...a, is_pinned: res.is_pinned } : a));
      if (activeArticleModal && activeArticleModal.id === id) {
        setActiveArticleModal(prev => ({ ...prev, is_pinned: res.is_pinned }));
      }
      loadThreatStats();
      showToast(res.message, 'success');
    } catch (err) {
      showToast('Failed to toggle pin state.', 'error');
    }
  };

  // Interactive Filter Handlers for cross-component triggers
  const handleFilterCategory = (cat) => {
    setSelectedCategory(cat);
    setPage(1);
    setActiveTab('feed');
  };

  const handleFilterSeverity = (sev) => {
    setSelectedSeverity(sev);
    setPage(1);
    setActiveTab('feed');
  };

  const handleFilterCve = (cve) => {
    setSearchQuery(cve);
    setPage(1);
    setActiveTab('feed');
  };

  // Header Title Metadata
  const getHeaderMeta = () => {
    switch (activeTab) {
      case 'feed':
        return {
          title: 'LIVE THREAT RADAR STREAM',
          subtitle: 'REAL-TIME INCIDENT INGESTION // 5 MULTI-THREADED INTEL FEEDS'
        };
      case 'dashboard':
        return {
          title: 'SOC OPERATIONS WAR ROOM',
          subtitle: 'THREAT TELEMETRY KPI MONITORING & CRITICAL EXPLOIT STATUS'
        };
      case 'pinned':
        return {
          title: 'PINNED THREATS VAULT',
          subtitle: 'BOOKMARKED ADVISORIES SAVED FOR IMMEDIATE INCIDENT RESPONSE'
        };
      case 'stats':
        return {
          title: 'THREAT INTELLIGENCE ANALYTICS',
          subtitle: 'RISK SPECTRUM, SOURCE METRICS & EXTRACTED CVE DATABASE'
        };
      case 'sources':
        return {
          title: 'LIVE INGESTION PIPELINES',
          subtitle: 'MONITORED RSS REPOSITORIES & REAL-TIME REFRESH CADENCE'
        };
      default:
        return { title: 'CYBERNEWS // AI', subtitle: 'LIVE THREAT PLATFORM' };
    }
  };

  const headerMeta = getHeaderMeta();
  const latestCriticalAlert = articles.find(a => a.severity === 'Critical') || null;

  return (
    <div className="app-container">
      
      {/* Sidebar Navigation */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          setActiveTab(tab);
          setPage(1);
        }}
        pinnedCount={threatStats?.pinned_count || 0}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Header 
          title={headerMeta.title}
          subtitle={headerMeta.subtitle}
          onRefresh={handleRefreshFeeds}
          isRefreshing={isRefreshing}
          lastSyncTime={lastSyncTime}
          autoPoll={autoPoll}
          onToggleAutoPoll={() => {
            const next = !autoPoll;
            setAutoPoll(next);
            showToast(`Auto-Poll ${next ? 'ACTIVATED (60s cadence)' : 'DEACTIVATED'}`);
          }}
          latestAlert={latestCriticalAlert}
        />

        <main className="page-wrapper">
          {activeTab === 'dashboard' && (
            <DashboardView 
              stats={threatStats}
              latestArticles={articles}
              onSelectTab={setActiveTab}
              onOpenArticle={setActiveArticleModal}
              onFilterCategory={handleFilterCategory}
              onFilterSeverity={handleFilterSeverity}
              onFilterCveOnly={(cveOnly) => {
                setHasCveFilter(cveOnly);
                setPage(1);
              }}
              onRefresh={handleRefreshFeeds}
              isRefreshing={isRefreshing}
            />
          )}

          {(activeTab === 'feed' || activeTab === 'pinned') && (
            <NewsFeedView 
              articles={articles}
              total={totalArticles}
              page={page}
              totalPages={totalPages}
              onPageChange={setPage}
              searchQuery={searchQuery}
              onSearchChange={(q) => { setSearchQuery(q); setPage(1); }}
              selectedCategory={selectedCategory}
              onCategoryChange={(cat) => { setSelectedCategory(cat); setPage(1); }}
              selectedSource={selectedSource}
              onSourceChange={(src) => { setSelectedSource(src); setPage(1); }}
              selectedSeverity={selectedSeverity}
              onSeverityChange={(sev) => { setSelectedSeverity(sev); setPage(1); }}
              hasCveFilter={hasCveFilter}
              onCveFilterChange={(val) => { setHasCveFilter(val); setPage(1); }}
              pinnedOnlyFilter={activeTab === 'pinned' ? true : pinnedOnlyFilter}
              onPinnedOnlyChange={(val) => { setPinnedOnlyFilter(val); setPage(1); }}
              categories={categories}
              sources={sources}
              onOpenArticle={setActiveArticleModal}
              onTogglePin={handleTogglePin}
              onRefresh={handleRefreshFeeds}
              isRefreshing={isRefreshing}
              isLoading={isLoadingArticles}
            />
          )}

          {activeTab === 'stats' && (
            <ThreatStatsView 
              stats={threatStats} 
              onFilterCategory={handleFilterCategory}
              onFilterSeverity={handleFilterSeverity}
              onFilterCve={handleFilterCve}
            />
          )}

          {activeTab === 'sources' && (
            <SourcesView 
              onRefresh={handleRefreshFeeds}
              isRefreshing={isRefreshing}
            />
          )}
        </main>
      </div>

      {/* Futuristic Article Detail Modal */}
      {activeArticleModal && (
        <ArticleDetailModal 
          article={activeArticleModal}
          onClose={() => setActiveArticleModal(null)}
          onTogglePin={handleTogglePin}
          onArticleUpdated={(updated) => {
            setArticles(prev => prev.map(a => a.id === updated.id ? updated : a));
            setActiveArticleModal(updated);
          }}
        />
      )}

      {/* Cyber Toast Notification */}
      {toast && (
        <div style={{
          position: 'fixed',
          bottom: '1.75rem',
          right: '1.75rem',
          background: toast.type === 'error' ? 'rgba(255, 51, 102, 0.95)' : 'rgba(8, 14, 26, 0.95)',
          border: toast.type === 'error' ? '1px solid #ff3366' : '1px solid var(--neon-cyan)',
          color: '#fff',
          padding: '0.85rem 1.4rem',
          borderRadius: 'var(--radius-sm)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 242, 254, 0.3)',
          zIndex: 2000,
          fontSize: '0.82rem',
          fontFamily: 'var(--font-mono)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.65rem',
          animation: 'slideUp 0.2s ease'
        }}>
          <span className="live-beacon"></span>
          <span>{toast.message}</span>
        </div>
      )}

    </div>
  );
}
