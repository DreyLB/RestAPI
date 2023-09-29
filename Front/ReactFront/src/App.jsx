import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [count, setCount] = useState(0);
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:5000/users")
      .then((response) => {
        setData(response.data);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Erro ao buscar os dados:", error);
      });
  }, []);

  useEffect(() => {
    console.log("teste:");
    console.log(data);
  }, [data]);

  return (
    <>
      <h2>Tabela clientes:</h2>
      <div className="container_clients">
        {data &&
          data.map((value) => (
            <div className="content_clients">
              <p>
                Nome: {value.name} <br />
                Email: {value.email} <br />
              </p>
            </div>
          ))}
      </div>
    </>
  );
}

export default App;
