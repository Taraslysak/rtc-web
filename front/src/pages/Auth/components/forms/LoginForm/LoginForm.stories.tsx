import { ComponentStory, ComponentMeta } from "@storybook/react";
import React from "react";

import { LoginForm } from "./LoginForm";

export default {
  title: "Components/LoginForm",
  component: LoginForm,
  args: {},
} as ComponentMeta<typeof LoginForm>;

const Template: ComponentStory<typeof LoginForm> = () => <LoginForm />;

export const Story = Template.bind({});
Story.args = {};
