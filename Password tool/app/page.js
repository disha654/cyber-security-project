"use client";

import { useMemo, useState } from "react";

const STRENGTH_LEVELS = [
  { label: "Very Weak", colorClass: "level-0" },
  { label: "Weak", colorClass: "level-1" },
  { label: "Fair", colorClass: "level-2" },
  { label: "Strong", colorClass: "level-3" },
  { label: "Very Strong", colorClass: "level-4" },
];

export default function HomePage() {
  const [activeTab, setActiveTab] = useState("analyzer");

  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [analyzeError, setAnalyzeError] = useState("");
  const [analyzing, setAnalyzing] = useState(false);

  const [inputs, setInputs] = useState({ name: "", nickname: "", dob: "", keyword: "" });
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState("");
  const [generatedMeta, setGeneratedMeta] = useState(null);

  const level = useMemo(() => {
    const score = analysis?.score ?? 0;
    return STRENGTH_LEVELS[Math.max(0, Math.min(4, score))];
  }, [analysis]);

  const progressWidth = analysis ? `${(analysis.score / 4) * 100}%` : "0%";

  const onInputChange = (key) => (event) => {
    setInputs((current) => ({ ...current, [key]: event.target.value }));
  };

  const analyzePassword = async () => {
    setAnalyzeError("");
    setAnalysis(null);

    if (!password.trim()) {
      setAnalyzeError("Enter a password to analyze.");
      return;
    }

    setAnalyzing(true);
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Analysis request failed.");
      }
      setAnalysis(payload);
    } catch (error) {
      setAnalyzeError(error.message || "Unable to analyze password right now.");
    } finally {
      setAnalyzing(false);
    }
  };

  const generateWordlist = async () => {
    setGenerateError("");
    setGeneratedMeta(null);

    const hasAnyInput = Object.values(inputs).some((value) => value.trim());
    if (!hasAnyInput) {
      setGenerateError("Provide at least one input value.");
      return;
    }

    setGenerating(true);
    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Generation request failed.");
      }
      setGeneratedMeta(payload);
    } catch (error) {
      setGenerateError(error.message || "Unable to generate wordlist right now.");
    } finally {
      setGenerating(false);
    }
  };

  const downloadWordlist = async () => {
    setGenerateError("");
    setGenerating(true);
    try {
      const response = await fetch("/api/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });

      if (!response.ok) {
        const payload = await response.json();
        throw new Error(payload.error || "Download request failed.");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "wordlist.txt";
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (error) {
      setGenerateError(error.message || "Unable to download wordlist.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <main className="ui-wrap">
      <section className="hero-block text-center">
        <span className="pill-tag">Security Toolkit</span>
        <h1 className="hero-heading">Password Strength Analyzer</h1>
        <p className="hero-copy">
          Analyze password security with entropy calculations and pattern detection. Generate custom attack
          wordlists for penetration testing.
        </p>

        <div className="tab-switcher" role="tablist" aria-label="Toolkit tabs">
          <button
            type="button"
            className={`tab-btn ${activeTab === "analyzer" ? "active" : ""}`}
            onClick={() => setActiveTab("analyzer")}
          >
            Password Analyzer
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === "generator" ? "active" : ""}`}
            onClick={() => setActiveTab("generator")}
          >
            Wordlist Generator
          </button>
        </div>
      </section>

      {activeTab === "analyzer" && (
        <section className="workspace">
          <div className="password-input-shell">
            <input
              type={showPassword ? "text" : "password"}
              className="password-input"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter password to analyze..."
            />
            <button type="button" className="ghost-btn" onClick={() => setShowPassword((v) => !v)}>
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>

          <div className="mt-3 text-center">
            <button className="btn btn-glow" type="button" onClick={analyzePassword} disabled={analyzing}>
              {analyzing ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" aria-hidden="true" />
                  Analyzing...
                </>
              ) : (
                "Analyze Password"
              )}
            </button>
          </div>

          {analyzeError && <div className="alert alert-danger mt-3 mb-0">{analyzeError}</div>}

          <article className="card result-card mt-4">
            <div className="card-body p-4 p-md-5">
              {!analysis ? (
                <div className="placeholder-state">
                  <div className="shield-mark">[]</div>
                  <h3>Enter a Password to Analyze</h3>
                  <p>
                    Type or paste a password above to get a comprehensive security analysis including entropy,
                    pattern detection, and improvement suggestions.
                  </p>
                </div>
              ) : (
                <div>
                  <div className="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
                    <h3 className="analysis-title mb-0">Analysis Results</h3>
                    <span className={`level-chip ${level.colorClass}`}>{level.label}</span>
                  </div>

                  <div className="d-flex justify-content-between small text-secondary mb-1">
                    <span>Strength Score</span>
                    <span>{analysis.score}/4</span>
                  </div>
                  <div className="progress dark-progress mb-4" role="progressbar" aria-label="Password strength">
                    <div
                      className={`progress-bar ${level.colorClass}`}
                      style={{ width: progressWidth }}
                    />
                  </div>

                  <div className="row g-3">
                    <div className="col-12 col-md-6">
                      <div className="info-box">
                        <div className="info-label">Crack Time</div>
                        <div className="info-value">{analysis.crack_time}</div>
                      </div>
                    </div>
                    <div className="col-12 col-md-6">
                      <div className="info-box">
                        <div className="info-label">Entropy</div>
                        <div className="info-value">{analysis.entropy} bits</div>
                      </div>
                    </div>
                  </div>

                  {analysis.warning && <div className="alert alert-warning mt-3 mb-0">Warning: {analysis.warning}</div>}

                  {analysis.suggestions?.length > 0 && (
                    <div className="suggestion-box mt-3">
                      <h4>Suggestions</h4>
                      <ul>
                        {analysis.suggestions.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </article>
        </section>
      )}

      {activeTab === "generator" && (
        <section className="workspace">
          <article className="card result-card">
            <div className="card-body p-4 p-md-5">
              <h3 className="analysis-title">Generate Custom Wordlist</h3>

              <div className="row g-3 mt-1">
                <div className="col-12 col-md-6">
                  <label className="form-label subtle-label">Name</label>
                  <input className="form-control dark-field" value={inputs.name} onChange={onInputChange("name")} />
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label subtle-label">Nickname</label>
                  <input className="form-control dark-field" value={inputs.nickname} onChange={onInputChange("nickname")} />
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label subtle-label">DOB</label>
                  <input
                    className="form-control dark-field"
                    value={inputs.dob}
                    onChange={onInputChange("dob")}
                    placeholder="2001"
                  />
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label subtle-label">Keyword</label>
                  <input className="form-control dark-field" value={inputs.keyword} onChange={onInputChange("keyword")} />
                </div>
              </div>

              <div className="d-flex gap-2 mt-4 flex-wrap">
                <button className="btn btn-glow" type="button" onClick={generateWordlist} disabled={generating}>
                  {generating ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" aria-hidden="true" />
                      Generating...
                    </>
                  ) : (
                    "Generate"
                  )}
                </button>
                <button
                  className="btn btn-outline-light"
                  type="button"
                  onClick={downloadWordlist}
                  disabled={generating || !generatedMeta}
                >
                  Download Wordlist (.txt)
                </button>
              </div>

              {generateError && <div className="alert alert-danger mt-3 mb-0">{generateError}</div>}

              {generatedMeta && (
                <div className="mt-4">
                  <div className="success-block">
                    Generated <strong>{generatedMeta.count.toLocaleString()}</strong> candidates.
                  </div>
                  <pre className="preview-box mt-3 mb-0">{generatedMeta.preview?.join("\n") || "No preview available."}</pre>
                </div>
              )}
            </div>
          </article>
        </section>
      )}
    </main>
  );
}
