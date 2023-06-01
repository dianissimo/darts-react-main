import "bootstrap/dist/css/bootstrap.min.css";
import styled from "styled-components";
import Card from "react-bootstrap/esm/Card";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import Button from "react-bootstrap/Button";
import {useNavigate} from "react-router-dom";
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';

export default function BlockContentCard(props) {
    const navigate = useNavigate();
    console.log(props.longreadData.longreadId)
    const longreadData = props.longreadData
    const chapterData = props.chapterData
    const blockData = props.blockData



    const handleClick = () => {
        console.log("clicked !")
        navigate(`/longreads/${longreadData.longreadId}/${chapterData.id}`, {
          state: {
            longreadData: longreadData,
            chapterData: chapterData
          }
        });
    };

    // const navigateToLongread = () => {
    //   console.log("clicked  navigateToLongread!")
    //   navigate(`/longreads/${longreadData.longreadId}`, {
    //     state: {
    //       longreadData: longreadData,
    //       chapterData: chapterData
    //     }
    //   });
    // };

    return (
    <Card
      style={{
        border: "none",
        boxShadow: "0 0 3px 0 rgba(0, 0, 0, 0.1)",
      }}
    >
      <Row gutters={0}>
        <Col md={10} className="d-flex flex-column">
          <Card.Body>
            {/* <Card.Title>{chapterData.name}</Card.Title> */}
            <Card.Text
              // style={{
              //   overflow: "hidden",
              //   display: "-webkit-box",
              //   WebkitLineClamp: "3",
              //   lineClamp: "3",
              //   WebkitBoxOrient: "vertical",
              //   textOverflow: "ellipsis",
              // }}
            >
              {blockData.text}
            </Card.Text>
          </Card.Body>
          <div
            className="mt-auto"
            style={{
              marginLeft: "15px",
              marginBottom: "15px",
            }}
          >
            
          </div>
        </Col>
        <Col
          md={2}
          style={{
            marginRight: "-15px",
          }}
        >
          <Card style={{
            border: "none",
            boxShadow: "0 0 10px 0 rgba(0, 0, 0, 0.1)",
          }}>
            <StyledButtonActive onClick={handleClick}>Edit</StyledButtonActive>
            <StyledButtonActive onClick={handleClick}>Delete</StyledButtonActive>
          {/* Here will be button to add event and to show Map */}
            <OverlayTrigger
              trigger="click"
              overlay={<Popover>
                <Popover.Body>
                  Add Event Form
                </Popover.Body>
              </Popover>}   
            >
              <StyledButtonActive variant="secondary">Add event</StyledButtonActive>
            </OverlayTrigger>


            <OverlayTrigger
              trigger="click"
              overlay={<Popover>
                <Popover.Body>
                  Delete Event Form
                </Popover.Body>
              </Popover>}   
            >
              <StyledButtonActive variant="secondary">Delete event</StyledButtonActive>
            </OverlayTrigger>

          </Card>
          
        </Col>
      </Row>
    </Card>
  );
}

const StyledButtonActive = styled(Button)`
  background-color: rgba(0, 81, 85, 1);
  border: none;
  border-radius: 4px;
  color: #ffffff;
  text-decoration: none;
  &:hover {
    background-color: rgba(0, 81, 85, 0.7);
    color: #ffffff;
  }
  &:active {
    background-color: rgba(0, 81, 85, 1) !important;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
    color: #ffffff;
  }
`;

const StyledImage = styled(Card.Img)`
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 4px;
`;
