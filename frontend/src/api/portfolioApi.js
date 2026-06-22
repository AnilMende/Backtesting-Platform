import axios from "axios";

const API = axios.create({
    baseURL : "http://127.0.0.1:8000"
});

export const runBacktest = async (params) => {

    const response = await API.get("/portfolio", {
        params
    });

    return response.data;
}