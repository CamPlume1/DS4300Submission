import React from 'react';
import './App.css';
import NickContainer from "./components/NickContainer";
import TomContainer from "./components/TomContainer";
import ReeceContainer from "./components/ReeceContainer";
import Stats from "./components/Stats";
import CamContainer from "./components/CamContainer";
/*

Main App Framework
Created by Cam Plume
 */
function App() {
  return (
     <div className="App">
      <header className="App-header">
        <h1>DS 4300: Retail Analytics App For Small Online Businesses</h1>
      </header>
        <Stats />
      <body className="App-body">
        <div className="image-grid">
          <CamContainer />
          <NickContainer />
          <TomContainer />
          <ReeceContainer />
        </div>
      </body>
      <footer className="App-footer">
        <p>Created By: Cameron Plume, Nicholas Perrotta, Tom McDonagh, Reece Calvin, and Andrew Enelow</p>
      </footer>
    </div>
  );
}

export default App;
