import { ComponentStory, ComponentMeta } from "@storybook/react";
import React from "react";

import { TextInput } from "./TextInput";

export default {
  title: "Components/TextInput",
  component: TextInput,
  args: {
    label: "string",
    value: "string",
    onChange: "any" as unknown as any,
    error: "string",
    disabled: "boolean" as unknown as any,
    type: "any" as unknown as any,
  },
} as ComponentMeta<typeof TextInput>;

const Template: ComponentStory<typeof TextInput> = (args) => (
  <TextInput {...args} />
);

export const Story = Template.bind({});
Story.args = {};
