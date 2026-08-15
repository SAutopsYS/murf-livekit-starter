'use client';

import type { ReactNode } from 'react';
import { type HTMLMotionProps, motion, useReducedMotion } from 'motion/react';
import { cn } from '@/lib/shadcn/utils';

const ENTER = [0.22, 1, 0.36, 1] as const;

function useMotionSafe() {
  const reduce = useReducedMotion();
  return {
    reduce: Boolean(reduce),
    duration: reduce ? 0 : 0.32,
    short: reduce ? 0 : 0.18,
  };
}

function Fade({ className, ...props }: HTMLMotionProps<'div'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration, ease: ENTER }}
      className={className}
      {...props}
    />
  );
}

function Rise({ className, ...props }: HTMLMotionProps<'div'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration, ease: ENTER }}
      className={className}
      {...props}
    />
  );
}

function Scale({ className, ...props }: HTMLMotionProps<'div'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration, ease: ENTER }}
      className={className}
      {...props}
    />
  );
}

function Slide({ className, ...props }: HTMLMotionProps<'div'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, x: 12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration, ease: ENTER }}
      className={className}
      {...props}
    />
  );
}

function Reveal({ className, ...props }: HTMLMotionProps<'div'>) {
  return <Rise className={cn(className)} {...props} />;
}

function Expand({ className, ...props }: HTMLMotionProps<'div'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={reduce ? undefined : { opacity: 0, height: 0 }}
      transition={{ duration, ease: ENTER }}
      className={cn('overflow-hidden', className)}
      {...props}
    />
  );
}

function Collapse(props: HTMLMotionProps<'div'>) {
  return <Expand {...props} />;
}

function PageTransition({ className, ...props }: HTMLMotionProps<'div'>) {
  return <Rise className={className} {...props} />;
}

function CardTransition({ className, ...props }: HTMLMotionProps<'article'>) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.article
      initial={reduce ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration, ease: ENTER }}
      className={className}
      {...props}
    />
  );
}

function DialogTransition({ className, ...props }: HTMLMotionProps<'div'>) {
  return <Scale className={className} {...props} />;
}

function ListAnimation({ children, className }: { children: ReactNode; className?: string }) {
  const { reduce, duration } = useMotionSafe();
  return (
    <motion.ul
      className={className}
      initial="hidden"
      animate="show"
      variants={{
        hidden: {},
        show: {
          transition: { staggerChildren: reduce ? 0 : 0.04 },
        },
      }}
    >
      {Array.isArray(children)
        ? children.map((child, index) => (
            <motion.li
              key={index}
              variants={{
                hidden: reduce ? { opacity: 1 } : { opacity: 0, y: 6 },
                show: { opacity: 1, y: 0, transition: { duration, ease: ENTER } },
              }}
            >
              {child}
            </motion.li>
          ))
        : children}
    </motion.ul>
  );
}

export {
  Fade,
  Rise,
  Scale,
  Slide,
  Reveal,
  Expand,
  Collapse,
  PageTransition,
  CardTransition,
  DialogTransition,
  ListAnimation,
  useMotionSafe,
};
