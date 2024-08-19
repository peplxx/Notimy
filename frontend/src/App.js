import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Index/>}/>
                <Route path="/j/:id" element={<JoinChannel/>}/>
                <Route path="/admin" element={<Admin/>} />
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
