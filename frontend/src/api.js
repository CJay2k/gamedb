import axios from 'axios';

export default axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
        // 'Authorization': "JWT " + localStorage.getItem('token')
    },
    // xsrfCookieName: 'csrftoken',
    // xsrfHeaderName: 'X-CSRFToken',
    // withCredentials: true
});