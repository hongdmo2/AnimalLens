/**
 * Button Component
 * 
 * A reusable button component that provides various styles and variants.
 * Built with Radix UI's Slot primitive and class-variance-authority for style variants.
 * 
 * Features:
 * - Multiple style variants (default, destructive, outline, secondary, ghost, link)
 * - Different sizes (default, sm, lg, icon)
 * - Support for asChild prop for composition
 * - Fully accessible and keyboard navigable
 * - Customizable via className prop
 */

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

// Define button style variants
const buttonVariants = cva(
  // Base button styles
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      // Style variants for different button types
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      // Size variants for different button sizes
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    // Default variant settings
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// Define button props interface
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean  // Prop for Radix UI Slot functionality
}

// Button component implementation
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"  // Use Slot component if asChild is true
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants } 