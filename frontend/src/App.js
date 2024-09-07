import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/app" element={<Index/>}/>
                <Route path="/j/:id" element={<JoinChannel/>}/>
                <Route path="app/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="app/admin" element={<Admin/>}/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
