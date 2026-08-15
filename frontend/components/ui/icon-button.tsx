import * as React from 'react';
import { type VariantProps } from 'class-variance-authority';
import { Button, buttonVariants } from '@/components/ui/button';

function IconButton({
  size = 'icon',
  ...props
}: React.ComponentProps<typeof Button> & VariantProps<typeof buttonVariants>) {
  return <Button size={size} {...props} />;
}

export { IconButton };
