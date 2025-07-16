<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Mouse Control Panel</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      background-color: #f4f4f4;
      color: #333;
      max-width: 900px;
      margin: auto;
      padding: 20px;
    }
    h1, h2, h3 {
      color: #0078D4;
    }
    code {
      background-color: #eaeaea;
      padding: 2px 6px;
      border-radius: 3px;
    }
    pre {
      background-color: #eaeaea;
      padding: 10px;
      border-radius: 5px;
      overflow-x: auto;
    }
    .screenshot {
      text-align: center;
      margin: 20px 0;
    }
    .screenshot img {
      max-width: 100%;
      border-radius: 8px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #eee;
    }
  </style>
</head>
<body>

  <h1>🖱️ Mouse Control Panel</h1>
  <blockquote>
    A lightweight desktop automation tool that simulates mouse activity to prevent idle timeouts, assists in auto-clicking, scheduled actions, and more — built with Python and Tkinter.
  </blockquote>

  <h2>✨ Features</h2>
  <ul>
    <li><strong>🔁 Auto Clicker:</strong> Toggle left-clicking at random intervals.</li>
    <li><strong>🌀 Mouse Nudging:</strong> Random movement to simulate human activity.</li>
    <li><strong>💾 Save Mouse Positions:</strong> Store up to <code>4</code> mouse locations.</li>
    <li><strong>🔄 Auto Cycling:</strong> Cycle through positions automatically.</li>
    <li><strong>⏱️ Scheduled Start:</strong> Begin automation after a delay.</li>
    <li><strong>⌨️ Hotkey Support:</strong> 
      <ul>
        <li><code>F7</code> → Save position</li>
        <li><code>F8</code> → Toggle clicking</li>
        <li><code>F9</code> → Toggle nudging</li>
        <li><code>ESC</code> → Panic stop</li>
      </ul>
    </li>
    <li><strong>🛠️ Settings Window:</strong> Configure click/nudge intervals and positions.</li>
    <li><strong>📦 Persistent Settings:</strong> Saved in local JSON files.</li>
    <li><strong>🧠 Manual Override Detection:</strong> Pauses automation during manual movement.</li>
    <li><strong>📥 Minimize to System Tray:</strong> Keeps the app out of the way.</li>
  </ul>

  <h2>📸 GUI Preview</h2>
  <div class="screenshot">
    <img src="https://via.placeholder.com/400x300.png?text=GUI+Preview+Coming+Soon" alt="Mouse Control Panel Screenshot">
  </div>

  <h2>🚀 Getting Started</h2>
  <h3>🔧 Prerequisites</h3>
  <pre><code>pip install pyautogui pystray pillow keyboard</code></pre>

  <h3>🛠️ Run the App</h3>
  <pre><code>python mouse_control_panel.py</code></pre>

  <h2>💡 Use Cases</h2>
  <ul>
    <li>Prevent system sleep or idle timeout.</li>
    <li>Keep VMs or remote sessions active.</li>
    <li>Automate repetitive screen tasks.</li>
    <li>Simulate user activity for testing software.</li>
  </ul>

  <h2>📁 Files</h2>
  <table>
    <tr>
      <th>File</th>
      <th>Description</th>
    </tr>
    <tr>
      <td><code>mouse_control_panel.py</code></td>
      <td>Main application script</td>
    </tr>
    <tr>
      <td><code>settings.json</code></td>
      <td>Stores click/nudge intervals and preferences</td>
    </tr>
    <tr>
      <td><code>mouse_positions.json</code></td>
      <td>Stores saved mouse positions</td>
    </tr>
  </table>

  <h2>🧠 Tips</h2>
  <ul>
    <li>Use tighter intervals for high-activity simulation.</li>
    <li>Cycle + Click = Persistent fake activity.</li>
    <li>Use Scheduled Start to activate while you're away.</li>
  </ul>

  <h2>🧰 Future Ideas</h2>
  <ul>
    <li>Hotkey remapping support</li>
    <li>Idle screen detection</li>
    <li>Custom click pattern templates</li>
    <li>Remote control via Telegram or Discord</li>
  </ul>

  <h2>🔒 Disclaimer</h2>
  <p>Use responsibly. This tool simulates user input and can interfere with other applications if misused.</p>

  <h2>🧑‍💻 Author</h2>
  <p>Developed by <strong>NorthFi</strong> — feel free to fork, improve, and contribute!</p>

</body>
</html>
