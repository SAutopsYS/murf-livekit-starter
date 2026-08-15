'use client';

import { Component, type ErrorInfo, type ReactNode } from 'react';
import { PageState, RetryAction } from '@/components/system/page-state';
import { reportError } from '@/lib/platform/errors';

type Props = { children: ReactNode };
type State = { failed: boolean };

export class PlatformErrorBoundary extends Component<Props, State> {
  state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    reportError(error, {
      boundary: 'os-shell',
      component: info.componentStack?.slice(0, 80) ?? '',
    });
  }

  render(): ReactNode {
    if (!this.state.failed) return this.props.children;
    return (
      <div className="flex min-h-[40vh] items-center justify-center p-6">
        <PageState
          kind="error"
          action={
            <RetryAction
              label="Reload"
              onClick={() => {
                this.setState({ failed: false });
              }}
            />
          }
        />
      </div>
    );
  }
}
