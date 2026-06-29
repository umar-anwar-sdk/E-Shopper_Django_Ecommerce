import React, { useState } from "react";
import { FaUser, FaLock, FaShieldAlt } from "react-icons/fa";
import logo from "../../assets/logo.png";
import { authService } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const navigate = useNavigate();
    // form state
    const [formData, setFormData] = useState({
      email: "",
      password: "",
    });

    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [debugResponse, setDebugResponse] = useState(null);

const handleChange = (e) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value,
  });
};

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  try {
    const res = await authService.login(formData);

    console.log(res.data);

    const access = res.data.access || res.data.tokens?.access;
    const refresh = res.data.refresh || res.data.tokens?.refresh;

    const userObj = res.data.user || res.data;
    const rawRole = userObj?.role || (userObj?.is_staff ? 'admin' : userObj?.is_vendor ? 'vendor' : res.data.role) || 'admin';
    const role = String(rawRole).toLowerCase();
    const userId = userObj?.id || userObj?.user_id || res.data.user_id || null;

    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('role', role);
    if (userId) localStorage.setItem('userId', String(userId));

    console.log('Saved Token:', localStorage.getItem('accessToken'));
    console.log('Saved Role:', localStorage.getItem('role'));

    if (role === 'vendor') {
      navigate('/vendor/dashboard');
    } else {
      navigate('/admin/dashboard');
    }
  } catch (err) {
    setErrorMessage("Login failed");
    console.log(err);
  }finally {
    console.log("Login attempt finished");
    setLoading(false);
  }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#1E293B] via-[#132a6b] to-[#1E293B]">
      
      <div className="w-[380px] rounded-2xl bg-[#f5f5f5]/90 shadow-2xl border border-white/10 p-8 backdrop-blur-md">

        <div className="flex justify-center mb-4">
          <img src={logo} alt="Logo" width={150} />
        </div>

        <h2 className="text-center text-[#1E293B] text-2xl font-semibold">
          Admin Portal
        </h2>
        <p className="text-center text-gray-700 text-sm mt-1">
          Enter your credentials to continue
        </p>

        <form onSubmit={handleSubmit}>

        <div className="mt-6">
          <label className="text-gray-700 text-sm">Email</label>
          <div className="flex items-center mt-2 bg-[#cdcdcd] rounded-lg px-3 py-2 border border-white/10">
            <FaUser className="text-[#1E293B] mr-2" />
            <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter email"
                className="bg-transparent w-full outline-none text-[#1E293B] placeholder-gray-700"
            />
          </div>
        </div>

        {/* Password */}
        <div className="mt-4">
          <label className="text-gray-700 text-sm">Password</label>
          <div className="flex items-center mt-2 bg-[#cdcdcd] rounded-lg px-3 py-2 border border-white/10">
            <FaLock className="text-[#1E293B] mr-2" />
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter password"
              className="bg-transparent w-full outline-none text-[#1E293B] placeholder-gray-700"
            />
          </div>
        </div>

        {/* Button */}
          <button type="submit" disabled={loading} className={`w-full mt-6 bg-blue-500 hover:bg-blue-600 transition-all text-white py-2.5 rounded-lg font-medium shadow-lg cursor-pointer disabled:opacity-70 ${loading ? "cursor-wait" : "cursor-pointer"}`}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          {errorMessage && (
            <div className="mt-3 text-sm text-red-600">{errorMessage}</div>
          )}

          {debugResponse && (
            <pre className="mt-3 text-xs text-gray-700 max-h-40 overflow-auto bg-white/80 p-2 rounded">{JSON.stringify(debugResponse, null, 2)}</pre>
          )}
        </form>
      </div>
    </div>
  );
};

export default Login;