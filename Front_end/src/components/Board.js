import React from "react";
import { Grid, Link } from "@material-ui/core";
import questionicon from "../images/questionicon.png";
import styled from "styled-components";

const StyledLink = styled(Link)`
  text-decoration: none;

  &:focus,
  &:visited,
  &:link,
  &:active {
    text-decoration: none;
  }

  &:hover {
    text-decoration: none;
    cursor: pointer;
  }
`;

const Board = ({ one }) => {
  const ctg = ["주식", "부동산", "펀드", "암호화폐", "기타"];
  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      style={{
        border: "1px solid #c8d0d0",
        borderRadius: "15px",
        marginBottom: "15px"
      }}
    >
      <Grid item xs={1}>
        <img
          src={questionicon}
          alt=""
          style={{
            width: "3rem",
            height: "auto",
            marginTop: "1rem",
            marginLeft: "1rem"
          }}
        />
      </Grid>
      <Grid item xs={10}>
        <StyledLink
          style={{
            color: "black"
          }}
          href={"/question/" + one.bnum}
        >
          <div>
            <h2 style={{ marginTop: "1.2rem" }}>
              [{ctg[one.bctg]}] {one.btitle}
            </h2>
            <p
              style={{
                display: "inline-block",
                lineHeight: "2rem",
                height: "4rem",
                textOverflow: "ellipsis",
                WebkitLineClamp: "2",
                WebkitBoxOrient: "vertical",
                // fontFamily: "Noto Serif KR",
                fontSize: "1rem",
                overflow: "hidden"
              }}
            >
              {one.bcontent}
            </p>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <p style={{ fontSize: "10px", marginRight: "10px" }}>
                작성자: {one.uid}
              </p>
              <p style={{ fontSize: "10px", marginRight: "10px" }}>
                조회수: {one.bhit}
              </p>
              <p style={{ fontSize: "10px" }}>생성일: {one.bcreation_date}</p>
            </div>
          </div>
        </StyledLink>
      </Grid>
    </Grid>
  );
};

export default Board;
