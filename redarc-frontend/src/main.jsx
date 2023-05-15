import React from 'react'
import ReactDOM from 'react-dom/client'
import Root from "./routes/root";
import Subreddit from "./routes/Subreddit";
import Thread from "./routes/Thread";
import Error from "./routes/Error";
//import App from './App.jsx'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorBoundary />
  },
  {
    path: "/r/:subreddit",
    element: <Subreddit/>,
    errorElement: <ErrorBoundary />
  },
  {
    path: "/r/:subreddit/comments/:threadID",
    element: <Thread/>,
    errorElement: <ErrorBoundary />
  },
  {
    path: "*",
    element: <Error/>,
  },
]);
function ErrorBoundary() {
  return <div>Error 500</div>;
}
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
