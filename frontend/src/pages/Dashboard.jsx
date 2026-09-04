import "./Dashboard.css";
import { useRef,useState } from "react";

function Dashboard() {

    const[data, setData] = useState(null);

    const fileInputRef = useRef(null);

    const handleSendClick = () => {
        // Opens the file picker
        fileInputRef.current.click();
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];

        if (!file) return;

        console.log("Selected file:", file);
        console.log("File name:", file.name);

        // Prepare file for backend
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:3000/api/dashboard/forecast", {
                method: "POST",
                body: formData,
            });

            setData(response);

            console.log("Backend response:", data);

        } catch (error) {
            console.error("Upload failed:", error);
        }
    };

  return (
    <div className="dashboard">


      <aside className="sidebar">

        <div className="logo-section">
          <div className="logo-icon">🛡</div>

          <div>
            <h2>SENTINEL-X</h2>
            <span>NETWORK FORECASTING</span>
          </div>
        </div>

        <div className="menu">

          <div className="menu-item active">
            <span>▣</span>
            Dashboard
          </div>

          <div className="menu-item">
            <span>◩</span>
            Analyze
          </div>

          <div className="menu-item">
            <span>◷</span>
            History
          </div>

          <div className="menu-item">
            <span>⚙</span>
            Settings
          </div>

        </div>

        <div className="sidebar-status">
          <span className="status-dot"></span>

          <div>
            <small>System Status</small>
            <strong>ONLINE</strong>
          </div>
        </div>

      </aside>




      <main className="main-content">

       

        <header className="topbar">

          <div className="page-title">
            <span className="hamburger">☰</span>
            <h1>DASHBOARD</h1>
          </div>

          <div className="top-right">

            <div className="online">
              <span className="status-dot"></span>
              SYSTEM ONLINE
            </div>

            <div className="time">
              14:05:32
            </div>

            <div className="refresh">
              ⟳
            </div>

          </div>

        </header>


        

        <section className="top-cards">

          

          <div className="card risk-card">

            <div className="card-label">
              CURRENT RISK
            </div>

            <div className="risk-value orange">
              {data ? `${data.current_attack_probability*100}%` : "Loading..."}
            </div>

            <div className="risk-status orange-text">
              Moderate
            </div>

            <div className="mini-trend">
              ↗
            </div>

          </div>


        

          <div className="card risk-card">

            <div className="card-label">
              FUTURE RISK <span>(Next 5 Windows)</span>
            </div>

            <div className="risk-value red">
                {data ? `${data.future_attack_probability*100}%` : "Loading..."}
            </div>

            <div className="risk-status red-text">
              High
            </div>

          </div>


         

          <div className="card stage-card">

            <div className="card-label">
              ATTACK STAGE
            </div>

            <div className="stage-value yellow">
              {data ? data.current_attack_type : "Loading..."}
            </div>

            <div className="stage-sub">
              (Current)
            </div>

          </div>


         

          <div className="card stage-card">

            <div className="card-label">
              PREDICTED NEXT STAGE
            </div>

            <div className="stage-value purple">
              {data ? data.future_attack_type : "Loading..."}
            </div>

            <div className="stage-sub">
              (74% Confidence)
            </div>

          </div>

        </section>


        

        <section className="dashboard-grid">


         

          <div className="card forecast-card">

            <div className="section-title">
              RISK FORECAST
              <span>(Next 5 Windows)</span>
            </div>

            <div className="chart">

              <div className="y-axis">
                <span>100%</span>
                <span>80%</span>
                <span>60%</span>
                <span>40%</span>
                <span>20%</span>
                <span>0%</span>
              </div>

              <div className="chart-area">

                <div className="grid-line line-1"></div>
                <div className="grid-line line-2"></div>
                <div className="grid-line line-3"></div>
                <div className="grid-line line-4"></div>
                <div className="grid-line line-5"></div>


                <svg
                  className="forecast-svg"
                  viewBox="0 0 500 230"
                  preserveAspectRatio="none"
                >

                  <polyline
                    points="25,180 130,135 245,100 360,58 465,38"
                    fill="none"
                    stroke="#ff8a00"
                    strokeWidth="4"
                  />

                  <circle
                    cx="25"
                    cy="180"
                    r="6"
                    fill="#ff8a00"
                  />

                  <circle
                    cx="130"
                    cy="135"
                    r="6"
                    fill="#ff8a00"
                  />

                  <circle
                    cx="245"
                    cy="100"
                    r="6"
                    fill="#ff8a00"
                  />

                  <circle
                    cx="360"
                    cy="58"
                    r="6"
                    fill="#ff8a00"
                  />

                  <circle
                    cx="465"
                    cy="38"
                    r="6"
                    fill="#ff4650"
                  />

                </svg>


                <div className="point-label p1">
                  32%
                </div>

                <div className="point-label p2">
                  45%
                </div>

                <div className="point-label p3">
                  58%
                </div>

                <div className="point-label p4">
                  70%
                </div>

                <div className="point-label p5">
                  78%
                </div>


                <div className="x-axis">
                  <span>NOW</span>
                  <span>+1</span>
                  <span>+3</span>
                  <span>+4</span>
                  <span>+5</span>
                </div>

              </div>

            </div>

          </div>


          

          <div className="card progression-card">

            <div className="section-title">
              ATTACK PROGRESSION
            </div>

            <div className="progression">

              <div className="attack-step current">

                <div className="attack-icon">
                  ◉
                </div>

                <span>
                  Reconnaissance
                </span>

                <small>
                  CURRENT
                </small>

              </div>


              <div className="arrow">
                →
              </div>


              <div className="attack-step predicted">

                <div className="attack-icon">
                  ⌕
                </div>

                <span>
                  Scanning
                </span>

                <small>
                  PREDICTED
                </small>

              </div>


              <div className="arrow">
                →
              </div>


              <div className="attack-step">

                <div className="attack-icon">
                  ☠
                </div>

                <span>
                  Exploitation
                </span>

              </div>


              <div className="arrow">
                →
              </div>


              <div className="attack-step">

                <div className="attack-icon">
                  ?
                </div>

                <span>
                  Impact
                </span>

              </div>

            </div>

          </div>


          <div className="card prediction-card">

            <div className="section-title">
              WHY THIS PREDICTION
              <span>(Top Contributing Features)</span>
            </div>

            <div className="features">


              <div className="feature-row">

                <span>SYN Rate</span>

                <div className="feature-bar">
                  <div
                    className="feature-fill orange-bar"
                    style={{ width: "95%" }}
                  ></div>
                </div>

                <span className="feature-value">
                  34%
                </span>

              </div>


              <div className="feature-row">

                <span>Unique Ports</span>

                <div className="feature-bar">
                  <div
                    className="feature-fill yellow-bar"
                    style={{ width: "82%" }}
                  ></div>
                </div>

                <span className="feature-value">
                  29%
                </span>

              </div>


              <div className="feature-row">

                <span>Packet Rate</span>

                <div className="feature-bar">
                  <div
                    className="feature-fill green-bar"
                    style={{ width: "58%" }}
                  ></div>
                </div>

                <span className="feature-value">
                  18%
                </span>

              </div>


              <div className="feature-row">

                <span>Flow Duration</span>

                <div className="feature-bar">
                  <div
                    className="feature-fill blue-bar"
                    style={{ width: "40%" }}
                  ></div>
                </div>

                <span className="feature-value">
                  9%
                </span>

              </div>


              <div className="feature-row">

                <span>Destination Entropy</span>

                <div className="feature-bar">
                  <div
                    className="feature-fill purple-bar"
                    style={{ width: "45%" }}
                  ></div>
                </div>

                <span className="feature-value">
                  10%
                </span>

              </div>

            </div>

          </div>


          

          <div className="card traffic-card">

            <div className="section-title">
              TRAFFIC STATISTICS
              <span>(Current Window)</span>
            </div>

            <div className="traffic-grid">


              <div className="stat-box">

                <div className="stat-icon">
                  ◉
                </div>

                <div>
                  <div className="stat-label">
                    Flows
                  </div>

                  <div className="stat-value">
                    12,430
                  </div>
                </div>

              </div>


              <div className="stat-box">

                <div className="stat-icon">
                  ▣
                </div>

                <div>
                  <div className="stat-label">
                    Packets
                  </div>

                  <div className="stat-value">
                    84K
                  </div>
                </div>

              </div>


              <div className="stat-box">

                <div className="stat-icon">
                  ▤
                </div>

                <div>
                  <div className="stat-label">
                    Bytes
                  </div>

                  <div className="stat-value">
                    12.4 MB
                  </div>
                </div>

              </div>


              <div className="stat-box">

                <div className="stat-icon">
                  ◷
                </div>

                <div>
                  <div className="stat-label">
                    Duration
                  </div>

                  <div className="stat-value">
                    5 min
                  </div>
                </div>

              </div>


            </div>

          </div>

        </section>

        <div className="file-upload">
            <div>Choose a file</div>
            {/* Hidden file input */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
            />

            {/* Your Send button */}
            <button onClick={handleSendClick}>
                Send
            </button>
        </div>

      </main>

    </div>
  );
}

export default Dashboard