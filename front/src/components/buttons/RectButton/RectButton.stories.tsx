import { ComponentStory, ComponentMeta } from "@storybook/react";
import React from "react";

import { RectButton } from "./RectButton";

export default {
  title: "Components/RectButton",
  component: RectButton,
  args: {
    title: "string",
    onClick: () => {},
    disabled: false,
    loading: false,
  },
} as ComponentMeta<typeof RectButton>;

const Template: ComponentStory<typeof RectButton> = (args) => (
  <RectButton {...args} />
);

export const Story = Template.bind({});
Story.args = {};
