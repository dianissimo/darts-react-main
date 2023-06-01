import React, {useEffect, useState} from "react";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import Card from "react-bootstrap/esm/Card";
import styled from "styled-components";
import WorldCard from "../components/WorldCard";
import axios from "axios";
import LongreadCard from "../components/LongreadCard.jsx";

export default function Worlds() {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [worlds, setWorlds] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/worlds/')
        .then(response => {
          setLoading(false);
          setWorlds(response.data);
        })
        .catch(error => {
          setLoading(false);
          console.error('Error fetching worlds:', error);
          setError('Error fetching worlds' + error.message);
        });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div id="worlds">
      <Container>
        <Row xs={1} sm={2} md={2} lg={3} xl={4} className="g-4">
          <Col xs={12} sm={12} md={12} lg={12} xl={12}>
            <Card
              className="bg-dark text-white"
              style={{
                border: "none",
                height: "300px",
              }}
            >
              <StyledImage src="../assets/samurai.jpg" />
              <Card.ImgOverlay>
                <Card.Title>The Last Samurai</Card.Title>
                <Card.Text>___________________</Card.Text>
                <Card.Text>Editor's pick</Card.Text>
              </Card.ImgOverlay>
            </Card>
          </Col>
          {worlds.map(world => (
              <Col>
                <WorldCard
                    id={world.id}
                    title={world.name}
                    desc={world.description}
                    img={world.img_link}
                />
              </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
}

const StyledImage = styled(Card.Img)`
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 4px;
`;
