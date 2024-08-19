// import axios from 'axios';

export const fetchOrders = async () => {
  console.log("fetching orders from API.");
  return [{id: 123, title: 'Bazzar', code: "BEBRA", messages: ['Hai!', 'Test '.repeat(50), 'Jopa :)', 'a'.repeat(15), 'a'.repeat(15), ]},
          {id: 456, title: 'Pizza', code: "PENIS", messages: ['a'.repeat(15), 'b'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), 'a'.repeat(15), ]}
          ]
  // const response = await axios.get(`${API_BASE_URL}/me`);
  // return response.data.orders;
};

export const joinChannel = async (id) => {
  return 'joint'
  // const response = await axios.post(`${API_BASE_URL}/join_channel/${id}`);
  // return response.data.order;
};

export const deleteOrderApi = async (id) => {
  return true;
}

export const createChannelAdmin = async () => {
    return true;
}

export const getMeAdmin = async () => {
    return {orders: [
        {id: 123, title: "BAZZAR", code: "A1B2C3",
            messages: ["Hi!", "Privet!", "JOPA()()()"]}
        ]};
}
