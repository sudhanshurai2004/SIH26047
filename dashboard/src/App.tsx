const stageOneChecklist = [
  "Frozen scenario, event, and doctrine contracts",
  "Local FastAPI service shell",
  "Offline development workflow"
];

export default function App() {
  return (
    <main className="shell">
      <section className="hero" aria-labelledby="page-title">
        <p className="eyebrow">SIH PS 26247 · OFFLINE TRAINING</p>
        <h1 id="page-title">AI-Enabled Drone &amp; Counter-Drone Threat Simulation Trainer</h1>
        <p className="lead">
          Stage 1 establishes the local contracts and development foundation. The trainee AAR
          dashboard is scheduled for Stage 3.
        </p>
      </section>

      <section className="status-card" aria-labelledby="foundation-title">
        <div>
          <p className="eyebrow">CURRENT FOUNDATION</p>
          <h2 id="foundation-title">No network, telemetry, weapon, or targeting interface</h2>
        </div>
        <ul>
          {stageOneChecklist.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
