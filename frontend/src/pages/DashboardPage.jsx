import React, { useState, useEffect } from 'react';
import '../css/DashboardPage.css';
import { Link, useParams } from 'react-router-dom';
import config from '../config.json';

// function DashboardPage() {
//   const [data, setData] = useState({});
//   const[email, setEmail] = useParams('');
// const email = useParams();


const DashboardPage = () => {
  const { email } = useParams();
  const [data, setData] = useState({});
  // console.log({email});

  // const fetchGitHubData = useCallback(({email}) => {
  //   // const Email = email;
  //   const GitHub_URL = config.GUTHUB_URL_DASHBOARD;
  //   // console.log(Email);
  //   fetch(GitHub_URL, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify({
  //       webhook: 'dashboard',
  //       emailId: {email},
  //     }),
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     setData(data);
  //     console.log(data);
  //   })
  //   .catch(error => {
  //     console.error(error);
  //   });
  // }, []);

  // useEffect(() => {
  //   const intervalId = setInterval(() => {
  //     fetchGitHubData(email);
  //   }, 10000);

  //   return () => {
  //     clearInterval(intervalId);
  //   };
  // }, [email, fetchGitHubData]);


  useEffect(() => {
    // const getEmail = () => email;
    const GitHub_URL = config.GUTHUB_URL_DASHBOARD;
    const intervalId = setInterval(() => {
      fetch(GitHub_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          // data to be sent to the Flask server
          webhook: 'dashboard',
          email
        }),
      })
        .then(response => response.json())
        .then(data => {
          setData(data);
          console.log(data)
        })
        .catch(error => {
          console.error(error);
        });
    }, 10000); // Send request every 10 seconds

    return () => {
      clearInterval(intervalId);
    };
  }, [email]);

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Request_id</th>
            <th>Action</th>
            <th>Author</th>
            <th>From_Branch</th>
            <th>To_Branch</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        {Object.keys(data).length > 0 &&
          <tbody>
            <tr>
              <td>{data._id}</td>
              <td>{data.request_id}</td>
              <td>{data.action}</td>
              <td>{data.author}</td>
              <td>{data.from_branch}</td>
              <td>{data.to_branch}</td>
              <td>{data.timestamp}</td>
            </tr>
          </tbody>}
      </table><br /><br />
      <div className='message'>
        {data.action === "PUSH" ? (
          <h3><b>Latest Changes: </b>{data.author} pushed to {data.to_branch} on {data.timestamp}</h3>
        ) : data.action === "PULL" ? (
          <h3><b>Latest Changes: </b>{data.author} submitted a pull request from {data.from_branch} to {data.to_branch} on{data.timestamp}</h3>
        ) : (
          <h3><b>Latest Changes: </b>{data.author} merged branch {data.from_branch} to {data.to_branch} on {data.timestamp}</h3>

        )}

      </div>
      <Link to="/"><button>Home</button> </Link>
    </div>
  );
}

export default DashboardPage;