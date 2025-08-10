import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import MachineDetail from './components/MachineDetail';
import Layout from './components/Layout';
import './index.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/machine/:id" element={<MachineDetail />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 