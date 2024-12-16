import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannelSpot from "./pages/JoinChannelSpot";
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";
import UUIDLogin from "./pages/UUID";
import {ProtectedRoute} from "./utils/protectedRoute";


function App() {
    // Main Entry
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/app" element={
                    <ProtectedRoute visitingForAdmin={false}>
                        <Index/>
                    </ProtectedRoute>
                }/>
                <Route path="/app/:token" element={<UUIDLogin />}/>
                <Route path="/j/:id" element={<JoinChannelSpot/>}/>
                <Route path="/j/c/:id" element={<JoinChannel/>}/>
                <Route path="/app/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="/app/admin" element={
                    <ProtectedRoute visitingForAdmin={true}>
                        <Admin/>
                    </ProtectedRoute>
                }/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
