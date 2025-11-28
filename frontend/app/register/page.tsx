'use client';
import React, { useState } from 'react';


const RegisterPage = () => {

    const[username, setUsername] = useState('');
    const[password, setPassword] = useState('');

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        const res=await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                 'Content-Type': "application/json",
            },
            body: JSON.stringify({username:username, password:password}),
        });
        const data = await res.json();
        console.log('user created',data);
    }

  return (
     <div className=''>
      <form action="" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="">username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="">password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  )
}

export default RegisterPage