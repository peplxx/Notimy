import React, {useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import {joinChannelSpot} from "../utils/api";

const JoinChannelSpot = () => {
    const {id} = useParams();
    const navigate = useNavigate();
    useEffect(() => {
        const joinAndNavigate = async () => {
            try {
                await joinChannelSpot(id);
                navigate('/app'); // Redirect after joining the channel
            } catch (error) {
                console.error("Failed to join channel", error);
                // Handle error as needed
            }
        };

        joinAndNavigate();
    }, [id, navigate]);

    return <div>adding channel</div>;
};

export default JoinChannelSpot;
