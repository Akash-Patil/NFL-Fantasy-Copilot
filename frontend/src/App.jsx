import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [position, setPosition] = useState('WR');
  const [scoring, setScoring] = useState('PPR');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Update this to your backend URL
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleCompare = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/start-sit`, {
        players: [player1.trim(), player2.trim()],
        position: position,
        scoring: scoring
      });
      
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to compare players. Check your backend connection.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Render stats dynamically based on position
  const renderPlayerStats = (stats, position) => {
    const statConfigs = {
      WR: [
        { label: 'PPG', key: 'ppg' },
        { label: 'Targets/G', key: 'targets_per_game' },
        { label: 'Rec/G', key: 'receptions_per_game' },
        { label: 'Yards/G', key: 'yards_per_game' },
        { label: 'Target Share', key: 'target_share_pct', suffix: '%' },
        { label: 'Y/TA', key: 'yards_per_team_att' }
      ],
      QB: [
        { label: 'PPG', key: 'ppg' },
        { label: 'Pass Yds/G', key: 'passing_yards_per_game' },
        { label: 'Pass TDs/G', key: 'passing_tds_per_game' },
        { label: 'INTs/G', key: 'interceptions_per_game' },
        { label: 'Comp %', key: 'completion_pct', suffix: '%' },
        { label: 'Rush Yds/G', key: 'rushing_yards_per_game' }
      ],
      RB: [
        { label: 'PPG', key: 'ppg' },
        { label: 'Rush Yds/G', key: 'rushing_yards_per_game' },
        { label: 'Rec/G', key: 'receptions_per_game' },
        { label: 'Carries/G', key: 'carries_per_game' },
        { label: 'YPC', key: 'yards_per_carry' },
        { label: 'Rec Yds/G', key: 'receiving_yards_per_game' }
      ],
      TE: [
        { label: 'PPG', key: 'ppg' },
        { label: 'Targets/G', key: 'targets_per_game' },
        { label: 'Rec Yds/G', key: 'receiving_yards_per_game' },
        { label: 'Rec/G', key: 'receptions_per_game' },
        { label: 'RZ Tgt/G', key: 'redzone_targets_per_game' },
        { label: 'Target Share', key: 'target_share_pct', suffix: '%' }
      ]
    };

    const config = statConfigs[position] || statConfigs.WR;

    return config.map((stat, idx) => (
      <div key={idx} className="stat">
        <span className="stat-label">{stat.label}</span>
        <span className="stat-value">
          {stats[stat.key]?.toFixed(1) || '0.0'}{stat.suffix || ''}
        </span>
      </div>
    ));
  };

  // No longer needed - API returns structured data!
  // const parseRecommendation = ... (removed)
  // const extractWinner = ... (removed)
  // const extractConfidence = ... (removed)
  // const extractReason = ... (removed)

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🏈 Fantasy Copilot</h1>
          <p>Compare players and get AI-powered recommendations</p>
        </header>

        <form onSubmit={handleCompare} className="form">
          {/* Position and Scoring Selectors at Top */}
          <div className="selectors">
            <div className="selector-group">
              <label htmlFor="position">🏈 Position</label>
              <select 
                id="position"
                value={position} 
                onChange={(e) => setPosition(e.target.value)}
                className="select"
              >
                <option value="WR">WR - Wide Receiver</option>
                <option value="QB">QB - Quarterback</option>
                <option value="RB">RB - Running Back</option>
                <option value="TE">TE - Tight End</option>
              </select>
            </div>

            <div className="selector-group">
              <label htmlFor="scoring">📊 Scoring Format</label>
              <select 
                id="scoring"
                value={scoring} 
                onChange={(e) => setScoring(e.target.value)}
                className="select"
              >
                <option value="PPR">PPR (Point Per Reception)</option>
                <option value="Half-PPR">Half-PPR (0.5 PPR)</option>
                <option value="Standard">Standard (No PPR)</option>
              </select>
            </div>
          </div>

          {/* Player Input Boxes */}
          <div className="input-group">
            <input
              type="text"
              placeholder="Player 1 (e.g., Tyreek Hill)"
              value={player1}
              onChange={(e) => setPlayer1(e.target.value)}
              required
              className="input"
            />
            <span className="vs">VS</span>
            <input
              type="text"
              placeholder="Player 2 (e.g., Justin Jefferson)"
              value={player2}
              onChange={(e) => setPlayer2(e.target.value)}
              required
              className="input"
            />
          </div>
          
          <button 
            type="submit" 
            disabled={loading}
            className="button"
          >
            {loading ? 'Analyzing...' : 'Compare Players'}
          </button>
        </form>

        {error && (
          <div className="error">
            <p>⚠️ {error}</p>
          </div>
        )}

        {result && (
          <div className="results">
            <div className="recommendation-header">
              <h2>
                Start: <span className="winner">{result.decision}</span>
              </h2>
              <div className={`confidence-badge confidence-${result.confidence.toLowerCase()}`}>
                Confidence: {result.confidence}
              </div>
            </div>

            <div className="reason">
              <strong>Why?</strong> {result.reason}
            </div>

            <div className="stats-comparison">
              <h3>Player Statistics</h3>
              <div className="stats-grid">
                {/* Player 1 Card */}
                <div className={`player-card ${result.decision === result.player1_stats.name ? 'winner' : ''}`}>
                  <h4>
                    {result.player1_stats.name} 
                    {result.decision === result.player1_stats.name && ' ⭐'}
                  </h4>
                  <div className="stats">
                    {renderPlayerStats(result.player1_stats, result.position)}
                  </div>
                  {result.player1_advantages.length > 0 && (
                    <div className="advantages">
                      <strong>Advantages:</strong> {result.player1_advantages.join(', ')}
                    </div>
                  )}
                </div>

                {/* Player 2 Card */}
                <div className={`player-card ${result.decision === result.player2_stats.name ? 'winner' : ''}`}>
                  <h4>
                    {result.player2_stats.name}
                    {result.decision === result.player2_stats.name && ' ⭐'}
                  </h4>
                  <div className="stats">
                    {renderPlayerStats(result.player2_stats, result.position)}
                  </div>
                  {result.player2_advantages.length > 0 && (
                    <div className="advantages">
                      <strong>Advantages:</strong> {result.player2_advantages.join(', ')}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
