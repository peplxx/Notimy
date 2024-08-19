import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {joinChannel} from "../utils/api";

const OrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const joinAndNavigate = async () => {
      try {
        await joinChannel(id);
        console.log('Id For Join: ' + id);
        navigate('/'); // Redirect after joining the channel
      } catch (error) {
        console.error("Failed to join channel", error);
        // Handle error as needed
      }
    };

    joinAndNavigate();
  }, [id, navigate]);

  return <div>Adding order...</div>;
};

export default OrderDetails;
