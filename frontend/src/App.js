import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Footer from './components/Footer';
import Home from './components/HomeRoute';
import Navbar from './components/Navbar.js';
import styled from 'styled-components';

const GlobalWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const MainWrapper = styled.div`
  flex: 1;
`;

function App() {
  return (
    <Router>
      <GlobalWrapper>
        <Navbar />
        <MainWrapper>
          <Routes>
            <Route path='/' element={Home} />
          </Routes>
        </MainWrapper>
        <Footer />
      </GlobalWrapper>
    </Router>
  );
}

export default App;
