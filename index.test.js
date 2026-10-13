// __tests__/index.test.js
import { render, screen, fireEvent } from "@testing-library/react";
import Home from "../pages/index";
import React from 'react';

describe("Home Page", () => {
  it("submits the form with a valid company URL", () => {
    render(<Home />);

    const input = screen.getByPlaceholderText("enter company url:");
    const button = screen.getByText("generate!");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.click(button);

    expect(window.alert).toHaveBeenCalledWith(
      expect.stringContaining("url submitted: https://example.com")
    );
  });

  it("shows an error for an invalid company URL", () => {
    render(<Home />);

    const input = screen.getByPlaceholderText("enter company url:");
    const button = screen.getByText("generate!");

    fireEvent.change(input, { target: { value: "invalid-url" } });
    fireEvent.click(button);

    expect(window.alert).toHaveBeenCalledWith(
      "please enter a valid url or resume!"
    );
  });
});
